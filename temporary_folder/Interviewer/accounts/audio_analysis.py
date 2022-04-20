import os
import speech_recognition as sr
import ffmpeg
from pydub import AudioSegment 
from pydub.utils import make_chunks
import os
 

def process_audio(path,rel_path):
	i = 0
	j = len(path)
	while i < j:
		file_path = path[i][1]
		destin_path = rel_path +"audioData\\"
		com1 = f"ffmpeg -i {file_path} {destin_path}\\{path[i][0]}.wav"
		os.system(com1)
		myaudio = AudioSegment.from_file(f"{destin_path}\\{path[i][0]}.wav", "wav") 
		chunk_length_ms = 8000 # pydub calculates in millisec 
		chunks = make_chunks(myaudio,chunk_length_ms) #Make chunks of one sec 
		for idx, chunk in enumerate(chunks): 
			chunk_name = f'{destin_path}' + f"{path[i][0]}" + "_{0}.wav".format(idx) 
			chunk.export(chunk_name, format="wav") 
		i +=1
