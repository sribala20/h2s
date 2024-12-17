# Hum-to-Search
![Thumbnail](https://raw.githubusercontent.com/sribala20/h2s/main/assets/demo.png)

This hum to search music recognization app identifies songs based on hummed or sung melodies using vector search in AstraDB and Spotify's [basic pitch](https://basicpitch.spotify.com/) to transform audio to MIDI and help to create vector embeddings. 

## Getting Started

To get started with this project and run it locally, follow the steps below:

* install Python 3.10.0 - the packages are stable on this version
* Node.js
* ffmpeg for audio processing

1. Clone the repository `git clone https://github.com/sribala20/h2s.git`
2. Change directory (`cd`) into the cloned repository flask backend `cd h2s/flask-api`
3. Rename `.env.example` to `.env` and fill in the required environment variables
   - To fill this in, you'll need an [Astra DB account](https://astra.datastax.com/)

## Ingesting the Data
Create a serveless vector database in AstraDB and a vector collection. Name the collection song_data, select vector-enabled collection, "Bring my own" for embedding generation method, input 128 dimensions, and Cosine similarity metric. Populate `.env` with the database connection details. 

```bash
# Navigate to our backend
cd ./flask-api

# Create a virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Export environmental variables
export ASTRA_DB_APPLICATION_TOKEN= ...
export ASTRA_DB_API_ENDPOINT= ...

# Run the script
python3 loadData.py
```
When this script runs, it will ingest the data from song_data.csv into your Astra database.

## Start up the App

1. `cd ./flask-api` type `flask run` in the command line. This will start our server locally.
3. Open up a new command line and in `/h2s` and run `npm install`.
4. Copy .env-frontend to .env and add the backend URL of the flask application.
5. Type `npm start` to start up the local development server. 

From here, you'll be able to run the project locally, so feel free to contribute or use it as a foundation for various projects.

## Resources
Here was the material that aided in building this app. 

**Query by Humming and Audio Embeddings**
- [MeloDetective with Vector Search and DTW](https://medium.com/@stannor/shazam-for-melodies-how-i-built-melodetective-with-vector-search-and-dtw-7185f54dcb56)
- [Audio Embeddings: Understanding the basics](https://dev.to/josethz00/audio-embeddings-understanding-the-basics-4pc1)
- [Patel, Parth, "Music Retrieval System Using Query-by-Humming" (2019). Master's Projects. 895.](https://doi.org/10.31979/etd.mh97-77wx)
- [Name That Tune: A Pilot Study in Finding a Melody From
a Sung Query](https://deepblue.lib.umich.edu/bitstream/handle/2027.42/35292/10373_ftp.pdf?sequence=1)
- [What is an Audio Embedding Model?](https://huggingface.co/blog/cappuch/audio-embedding-wtf)
- [Kaggle top 10000 spotify songs dataset](https://www.kaggle.com/datasets/joebeachcapital/top-10000-spotify-songs-1960-now/data)

**In-app recording**
- [Record Your MIC with JavaScript](https://www.youtube.com/watch?v=3OnMBtOyGkY)
- [An introduction to the MediaRecorder API](https://www.twilio.com/en-us/blog/mediastream-recording-api)


### Contributions 

We accept pull requests and issues on this project. If you've got ideas, please **open an issue first** and discuss it with us and ideally it becomes a pull request that we open together. All contributions are welcome!
