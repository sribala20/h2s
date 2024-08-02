# Hum-to-Search

https://github.com/datastax/movies_plus_plus/assets/9947422/6e739836-dc25-4834-a5aa-e341a35d1559

This hum to search music recognization app identifies songs based on hummed or sung melodies using vector search on audio embeddings in AstraDB. 
Movies++ is a movie recommendation application that makes use of [GenAI](https://en.wikipedia.org/wiki/Generative_artificial_intelligence) to recommend movies based on natural language input. It is built on [DataStax Astra](https://astra.datastax.com/) and was demoed at [CascadiaJS](https://www.youtube.com/live/HfsNGyDQtJ4?si=XzDN5lzEcmIXncJ7&t=30203) and [DataStax's RAG++ AI Hack Night](https://www.datastax.com/events/rag-plus-plus-ai-hack-night-june-2024).

## Getting Started

To get started with this project and run it locally, follow the steps below:
pre-reqs:
* install Python 3.10.0 - the packages are stable on this version
* Node.js
* ffmpeg for audio processing

steps:
1. Clone the repository `git clone https://github.com/sribala20/h2s.git`
2. Change directory (`cd`) into the cloned repository flask backend `cd h2s/flask-api`
3. Rename `.env.example` to `.env` and fill in the required environment variables
   - To fill this in, you'll need an [Astra DB account](https://astra.datastax.com/)

## Ingesting the Data

Once you've populated `.env` with your API keys, make sure you have a collection in your Astra database named "movies". Once all those pieces are in place, you can run the following command to ingest the data:

```bash
# Navigate to our scripts
cd ./scripts

# Install dependencies
pip install -r requirements.txt

# Run the script
python load_movies.py
```

When this script runs, it will ingest the data from TMDB into your Astra database. This will allow you to search for movies and get recommendations based on the data you've ingested.

From here, you'll be able to run the project locally, so feel free to contribute or use it as a foundation for various projects.

## Working with Langflow

To use RAG with Langflow, you'll need to run Langflow. You can either do this as a [hosted cloud solution](https://langflow.datastax.com) on DataStax, or follow the [Langflow documentation](https://docs.langflow.org/) to get started running it locally.

## Contributing

We accept pull requests and issues on this project. If you've got ideas, please **open an issue first** and discuss it with us and ideally it becomes a pull request that we open together. All contributions are welcome!

### Contribution Ideas

If you'd like to contribute but don't know where to start, feel free to check out the [open issues](https://github.com/datastax/movies_plus_plus/issues) on this repository.