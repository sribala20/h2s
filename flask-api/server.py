from flask import Flask, request, jsonify
import requests
import subprocess
import numpy as np
import pretty_midi
import os
import multiprocessing
from astrapy import DataAPIClient
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH
from basic_pitch.note_creation import model_output_to_notes
#from flask_cors import CORS

app = Flask(__name__)
client = DataAPIClient(os.environ["ASTRA_DB_APPLICATION_TOKEN"])
database = client.get_database(os.environ["ASTRA_DB_API_ENDPOINT"])
collection = database.get_collection("no_norm")
#CORS(app)

app.config['DEBUG'] = True


@app.route('/songs', methods=['GET'])
def output_songs():
    try:
        songs = collection.find()
        song_list = [{'track': song['track'], 'artist': song['artist']} for song in songs]  # Assuming each song document has 'track' and 'artist' fields
        print(jsonify(song_list))
        return jsonify(song_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def audio_to_midi(audio_path: str, midi_path: str):
    # Predict the notes using the basic pitch model
    model_output, _, _ = predict(audio_path, ICASSP_2022_MODEL_PATH)

    # Convert model output to notes
    midi, note_events = model_output_to_notes(
        output=model_output,
        onset_thresh=0.5,
        frame_thresh=0.3,
        infer_onsets=True,
        min_note_len=11,
        min_freq=1,
        max_freq=3500,
        include_pitch_bends=True,
        multiple_pitch_bends=False,
        melodia_trick=True,
        midi_tempo=120
    )

    return midi

def normalize(v):
    norm = np.linalg.norm(v)
    return v / norm if norm != 0 else v

# Extract pitch vector
def get_pitch_vector(midi_data):
    pitch_vector = []
    for instrument in midi_data.instruments:
        for note in instrument.notes:
            pitch_vector.append(note.pitch)
    return pitch_vector

def create_note_histogram(pitches):
    histogram, _ = np.histogram(pitches, bins=np.arange(0, 129))
    norm_histogram = normalize(histogram)
    return norm_histogram


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['audioFile']
    temp_dir = '/Users/sri.bala/h2s/flask-api/temp'
    temp_audio_path = os.path.join(temp_dir, file.filename)
    file.save(temp_audio_path)

    midi_dir =  '/Users/sri.bala/h2s/flask-api/midi/output.mid'
    midi_data = audio_to_midi(temp_audio_path, midi_dir)
    pitches = get_pitch_vector(midi_data)
    emb = create_note_histogram(pitches)
    emb_str = np.array2string(emb, separator=',', formatter={'float_kind':lambda x: "%.5f" % x}).replace(' ', '')
    print("vector:", emb_str)
    results = collection.find(
    sort={"$vector": emb},
    limit=1)

    for doc in results:
        print (doc)
        res = doc


    print("Matching result:", res)  # Debugging statement

    os.remove(temp_audio_path)
    return jsonify({'track': res['track'],
                    'artist': res['artist'],
                    'album': res['album'],
                    'album_image': res['album_image'],
                    'track_url': res['track_url']})


if __name__ == '__main__':
    app.run(debug=True)