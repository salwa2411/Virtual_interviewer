from __future__ import absolute_import, unicode_literals
from celery import shared_task
from . import data_queue
from . import audio_emotion
from . import analysis
from . import audio_analysis
import os
import json
from .models import Profile
import datetime
from django.contrib.auth.models import User

audioEmotion = None
audioem = audio_emotion.livePredictions()

@shared_task
def anas(username, counter, path, id):
    tempuser = User.objects.filter(id=id).first()
    print(tempuser.id, tempuser.username)
    global audioEmotion
    data_queue.path.append((username+str(counter),path+username+str(counter)+".mp4"))
    print("in line 22")
    audio_analysis.process_audio(data_queue.path,path)
    model_loaded = audioem
    print("in line 27")

    audio_file_path =path+"audioData"
    files = os.listdir(audio_file_path)
    final_emotions = {"neutral": 0, "calm": 0, "happy": 0, "sad": 0, "angry": 0, "fearful": 0, "disgust": 0, "surprised": 0}
    print("before for loop", files)
    for file in files:
        print("in for loop", file)
        emotions = model_loaded.makepredictions(audio_file_path+"/"+file)
        final_emotions[emotions] += 1
    print("after predictions")
    dir = "../Interviewer/media/audioData/"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    total = sum(final_emotions.values())
    average = total//len(final_emotions)
    minimum_diff = float("inf")
    emotion = None
    print("after calculations")
    for key in final_emotions:
        if abs(final_emotions[key] - average) < minimum_diff and final_emotions[key] > 0:
            minimum_diff = abs(final_emotions[key] - average)
            emotion = key
    audioEmotion = emotion

    analysis.analyze(data_queue.path)

    with open('result.json') as json_data:
        data = json.load(json_data)
        
    length = len(data)
    for i in range(1, length+1):
        curr_user = username+str(i)
        face_emotion = data[curr_user]
        min_diff = float("inf")
        summ = sum(face_emotion.values())
        avg = summ//len(face_emotion)
        emt = None
        for i in face_emotion:
            if abs(face_emotion[i] - avg) < min_diff and face_emotion[i] > 0:
                min_diff = abs(face_emotion[i] - avg)
                emt = i

        profile_instance = Profile()
        profile_instance.user_id = tempuser
        profile_instance.date = datetime.datetime.now()
        profile_instance.facial_expressions_keys = list(face_emotion.keys())
        profile_instance.facial_expressions_values = list(face_emotion.values())
        profile_instance.audio_analysis_keys = list(final_emotions.keys())
        profile_instance.audio_analysis_values = list(final_emotions.values())
        profile_instance.average_face_emotions = emt
        profile_instance.average_audio_emotions = audioEmotion
        profile_instance.save()
    print(data_queue.path)
