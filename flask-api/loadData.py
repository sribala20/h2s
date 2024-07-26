import requests
import subprocess
import multiprocessing
import numpy as np
import pretty_midi
import pandas as pd
from astrapy import DataAPIClient
import os

song_data = pd.read_csv('/Users/sri.bala/hum-to-search/song_data.csv')
client = DataAPIClient(os.environ["ASTRA_DB_APPLICATION_TOKEN"])
database = client.get_database(os.environ["ASTRA_DB_API_ENDPOINT"])
collection = database.get_collection("midi_data")
num_cores = multiprocessing.cpu_count()

temp_dir = 'temp'
os.makedirs(temp_dir, exist_ok=True)

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

for index, row in song_data.iterrows():
    track = row['Track Name']
    artist = row['Artist Name(s)']
    album = row['Album Name']
    release_date = row['Album Release Date']
    album_image = row['Album Image URL']
    track_url = row['Track Preview URL']

    # write mp3 from track url
    response = requests.get(track_url)
    if response.status_code == 200:
        temp_audio_path = os.path.join(temp_dir, f"{index}.mp3")
        with open(temp_audio_path, 'wb') as f:
            f.write(response.content)
    
    # pip install demucs. isolates track vocals, created dir separated/htdemucs/idx
    demucs_command = f"python3 -m demucs.separate --two-stems=vocals -d cpu -j {num_cores} \"{temp_audio_path}\""
    subprocess.run(demucs_command, shell=True)
    vocals_path = os.path.join('separated/htdemucs',str(index),'vocals.wav')

    # pip install basic-pitch. translates audio to midi
    bp_command = f"basic-pitch --save-midi /Users/sri.bala/hum-to-search/midi \"{temp_audio_path}\""
    subprocess.run(bp_command, shell=True)
    midi_path = f"/Users/sri.bala/hum-to-search/midi/{index}_basic_pitch.mid"

    # get embedding
    midi_data = pretty_midi.PrettyMIDI(midi_path)
    pitches = get_pitch_vector(midi_data)
    emb = create_note_histogram(pitches)

    # insert embedding into collection
    try:
            inserted_song = collection.insert_one({
                "track": track,
                "artist": artist,
                "$vector": emb,
                "album": album,
                "date": release_date,
                "album_image": album_image,
                "track_url": track_url
            })
            print(f"* Inserted {(inserted_song)}\n")
   
    except Exception as e:
        print(f"Insert failed: {e}")
    
    os.remove(temp_audio_path) # storing mp3s temporarily
    os.remove(midi_path)

    



