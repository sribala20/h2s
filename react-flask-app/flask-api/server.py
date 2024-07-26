from flask import Flask, request, jsonify
import requests
import subprocess
import numpy as np
import pretty_midi
import os
from astrapy import DataAPIClient
#from flask_cors import CORS

app = Flask(__name__)
client = DataAPIClient(os.environ["ASTRA_DB_APPLICATION_TOKEN"])
database = client.get_database(os.environ["ASTRA_DB_API_ENDPOINT"])
collection = database.get_collection("midi_data")
#CORS(app)

app.config['DEBUG'] = True

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

@app.route('/', methods=['GET'])
def home():
    return "Hello, World!"

@app.route('/embeddings', methods=['POST'])
def get_data():
    return {'info': "Hello from Flask!"}

@app.route('/upload', methods=['POST'])
def upload():
    # data = request.get_json()
    # print("Received URL:", data['myData'])  # Debugging statement
    # track_url = data['myData']  # Corrected this line
    file = request.files['audioFile']
    temp_dir = '/Users/sri.bala/h2s/react-flask-app/flask-api/temp'
    temp_audio_path = os.path.join(temp_dir, file.filename)
    file.save(temp_audio_path)
    # response = requests.get(track_url)
    # if response.status_code == 200:
    #      with open(temp_audio_path, 'wb') as f:
    #         f.write(response.content)
            
    midi_dir =  '/Users/sri.bala/h2s/react-flask-app/flask-api/midi'
    subprocess.run(['basic-pitch', '--save-midi', midi_dir, temp_audio_path])
    midi_path = os.path.join(midi_dir, "recording_basic_pitch.mid")

    midi_data = pretty_midi.PrettyMIDI(midi_path)
    pitches = get_pitch_vector(midi_data)
    emb = create_note_histogram(pitches)
    emb_str = np.array2string(emb, separator=',', formatter={'float_kind':lambda x: "%.5f" % x}).replace(' ', '')
    print(emb_str)
    results = collection.find(
    sort={"$vector": emb},
    limit=5)

    for doc in results:
        print (doc)
        res = doc

    embedding_list = emb.tolist()

    print("Generated embedding:", res)  # Debugging statement
    os.remove(temp_audio_path)
    os.remove(midi_path)
    return jsonify({'track': res['track'],
                    'artist': res['artist'],
                    'album': res['album'],
                    'album_image': res['album_image'],
                    'track_url': res['track_url']})


if __name__ == '__main__':
    app.run(debug=True)