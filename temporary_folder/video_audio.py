import os
import speech_recognition as sr
import ffmpeg
from pydub import AudioSegment 
from pydub.utils import make_chunks
import os
 

def process_sudio(file_name):
	com1 = f"ffmpeg -i {file_name} speech.wav"
	os.system(com1)
	myaudio = AudioSegment.from_file("speech.wav", "wav") 
	chunk_length_ms = 8000 # pydub calculates in millisec 
	chunks = make_chunks(myaudio,chunk_length_ms) #Make chunks of one sec 
	for i, chunk in enumerate(chunks): 
		chunk_name = './chunked/' + file_name + "_{0}.wav".format(i) 
		print ("exporting", chunk_name) 
		chunk.export(chunk_name, format="wav") 

# all_file_names = os.listdir()
# try:
#     os.makedirs('chunked') # creating a folder named chunked
# except:
#     pass
# for each_file in all_file_names:
#     if ('.wav' in each_file):
os.makedirs('chunked')
process_sudio('sample.mp4')