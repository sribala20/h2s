from flask import Flask, request, jsonify
import os
import numpy as np
from astrapy import DataAPIClient
from getEmbeds import generate_embedding
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
client = DataAPIClient(os.environ["ASTRA_DB_APPLICATION_TOKEN"])
database = client.get_database(os.environ["ASTRA_DB_API_ENDPOINT"])
collection = database.get_collection("long_notes")

@app.route('/', methods=['GET'])
def hello():
    return "Hello World!"

@app.route('/songs', methods=['GET'])
def output_songs():
    try:
        response = [
    { "track": "In the End", "artist": "Linkin Park" },
    { "track": "Yellow", "artist": "Coldplay" },
    { "track": "Ride", "artist": "Twenty One Pilots" },
    { "track": "Fast Car", "artist": "Luke Combs" },
    { "track": "This Girl (Kungs Vs. Cookin' On 3 Burners)", "artist": "Kungs, Cookin' On 3 Burners" },
    { "track": "Hard Times", "artist": "Paramore" },
    { "track": "Electric Feel", "artist": "MGMT" },
    { "track": "Payphone", "artist": "Maroon 5, Wiz Khalifa" },
    { "track": "Tongue Tied", "artist": "GROUPLOVE" },
    { "track": "The Less I Know The Better", "artist": "Tame Impala" },
    { "track": "Little Talks", "artist": "Of Monsters and Men" },
    { "track": "vampire", "artist": "Olivia Rodrigo" },
    { "track": "Starboy", "artist": "The Weeknd, Daft Punk" },
    { "track": "Miss You", "artist": "Oliver Tree, Robin Schulz" },
    { "track": "Pompeii", "artist": "Bastille" },
    { "track": "Blank Space", "artist": "Taylor Swift" },
    { "track": "Watermelon Sugar", "artist": "Harry Styles" },
    { "track": "I'm Good (Blue)", "artist": "David Guetta, Bebe Rexha" },
    { "track": "Cupid - Twin Ver.", "artist": "FIFTY FIFTY" },
    { "track": "Unwritten", "artist": "Natasha Bedingfield" }
    ]
        return jsonify(response)
    except Exception as e:
        return jsonify({"error retrieving songs from Astra": str(e)}), 500


@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['audioFile']
        temp_dir = '/tmp/h2s/flask-api/temp'

        # Ensure the file path exists
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        temp_audio_path = os.path.join(temp_dir, file.filename)
        file.save(temp_audio_path) # Save the uploaded mp3 audio to the temp directory

        vector_embedding = generate_embedding(temp_audio_path)
        emb_str = np.array2string(vector_embedding, separator=',', formatter={'float_kind':lambda x: "%.20f" % x}).replace(' ', '')
        
        print("vector:", emb_str) # Debugging statement to see vector output
        
        # vector similiarity search
        results = collection.find(
        sort={"$vector": vector_embedding},
        limit=5)

        tracks = []
        for doc in results:
            tracks.append({
                'track': doc['track'],
                'artist': doc['artist'],
                'album': doc['album'],
                'album_image': doc['album_image'],
                'track_url': doc['track_url']
            })

        print("Matching result:", tracks)  # Debugging statement

        os.remove(temp_audio_path)

        response = jsonify({'tracks':tracks})
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response
    except Exception as e:
            return jsonify({"error uploading audio": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
    # port=8080 for google cloud run