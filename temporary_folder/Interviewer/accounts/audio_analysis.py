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
			# print ("exporting", chunk_name) 
			chunk.export(chunk_name, format="wav") 
		i +=1

# all_file_names = os.listdir()
# try:
#     os.makedirs('chunked') # creating a folder named chunked
# except:
#     pass
# for each_file in all_file_names:
#     if ('.wav' in each_file):
# os.makedirs(r'E:\Project-Testing\Virtual_interviewer\temporary_folder\Interviewer\media\audioData\chunked')
# process_sudio('usertest2.mp4',r'E:\Project-Testing\Virtual_interviewer\temporary_folder\Interviewer\media\audioData\\')