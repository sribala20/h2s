import os
import pyperclip
import numpy as np
from getEmbeds import generate_embedding

'''
go to AstraDB and paste your embedding in the collection search bar to see the similarity search run!
'''

temp_audio_path = './hums/5.mp3' # Path to a test file
emb = generate_embedding(temp_audio_path)

emb_str = np.array2string(emb, separator=',', formatter={'float_kind':lambda x: "%.5f" % x}).replace(' ', '')
pyperclip.copy(emb_str)
print("Embedding copied to clipboard.")


    



