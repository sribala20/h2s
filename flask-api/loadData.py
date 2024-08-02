import requests
import pandas as pd
import subprocess
import multiprocessing
from astrapy import DataAPIClient
import os
from getEmbeds import generate_embedding

song_data = pd.read_csv('./song_data.csv')
client = DataAPIClient(os.environ["ASTRA_DB_APPLICATION_TOKEN"])
database = client.get_database(os.environ["ASTRA_DB_API_ENDPOINT"])
collection = database.get_collection("song_data")
num_cores = multiprocessing.cpu_count()

temp_dir = 'temp'
os.makedirs(temp_dir, exist_ok=True)

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
    
    # creates folder separated/htdemucs/idx, clean up folder afterwards.
    demucs_command = f"python3 -m demucs.separate --two-stems=vocals -d cpu -j {num_cores} \"{temp_audio_path}\""
    subprocess.run(demucs_command, shell=True)
    vocals_path = os.path.join('separated/htdemucs',str(index),'vocals.wav')

    # convert vocals to embeddings
    emb = generate_embedding(vocals_path)

    # insert song with embedding into database
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


    



