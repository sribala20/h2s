import numpy as np
import os
from astrapy import DataAPIClient
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH
from basic_pitch.note_creation import model_output_to_notes

client = DataAPIClient(os.environ["ASTRA_DB_APPLICATION_TOKEN"])
database = client.get_database(os.environ["ASTRA_DB_API_ENDPOINT"])
collection = database.get_collection("no_norm")

def audio_to_midi(audio_path: str):
    model_output, _, _ = predict(audio_path, ICASSP_2022_MODEL_PATH)

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

# Function to extract pitches from MIDI data
def get_pitch_vector(midi_data):
    pitch_vector = []
    for instrument in midi_data.instruments:
        for note in instrument.notes:
            pitch_vector.append(note.pitch)
    return pitch_vector

# Function to normalize a vector
def normalize(v):
    norm = np.linalg.norm(v)
    return v / norm if norm != 0 else v

# Function to create a normalized note histogram from pitch data
def create_note_histogram(pitches):
    histogram, _ = np.histogram(pitches, bins=np.arange(0, 129))
    norm_histogram = normalize(histogram)
    return norm_histogram

# Function to generate embedding from audio file
def generate_embedding(temp_audio_path):
    midi_data = audio_to_midi(temp_audio_path)
    pitches = get_pitch_vector(midi_data)
    emb = create_note_histogram(pitches)
    return emb