import os
import pyperclip
import numpy as np
from getEmbeds import generate_embedding

'''
go to AstraDB and paste your embedding in the collection search bar to see the similarity search run!
'''

temp_audio_path = 'example.mp3' # Path to a test file
vector_embedding= generate_embedding(temp_audio_path)

emb_str = np.array2string(vector_embedding, separator=',', formatter={'float_kind':lambda x: "%.5f" % x}).replace(' ', '')
pyperclip.copy(emb_str)
print("Embedding copied to clipboard.")


    



