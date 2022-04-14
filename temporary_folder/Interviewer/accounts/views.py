from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm

from django.http.response import StreamingHttpResponse
# from accounts.camera import VideoCamera
import cv2
# from . import queue
import os
import json

from . import analysis
from . import data_queue
from . import audio_analysis
from . import audio_emotion
from accounts.models import Profile
import datetime


counter = 0
def home(request):

    return render(request,'index.html')
def registerUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            # print()
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                
                return redirect('login')
			
        context = {'form':form}
        return render(request, 'accounts/sign_login.html',context)
    # else:
    #     return render(request,'home.html')

def loginUser(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'accounts/sign_login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('home')

def takeInterview(request):
    if request.user.is_authenticated:
        questions = ["Tell me About Yourself", "Why should we hire you?", "What are your strengths and weaknesses?"]
        return render(request,'interview.html', {'questions': questions})
    return redirect('login')
audioEmotion = None
def temp(request):
    global audioEmotion
    global counter
    counter+=1
    path = os.getcwd() +r"\media\\"
    username = request.user.username
    if request.method == 'POST':
        print(request.body)

        with open(f"{path}"+f"{username}" + str(counter) + ".mp4", "wb") as test:
            test.write(request.body)

        # video = request.FILES['file']
        data_queue.path.append((username+str(counter),path+username+str(counter)+".mp4"))
        # print(data_queue.path)
        audio_analysis.process_audio(data_queue.path,path)
        # model_dir = path + "static\\model\\testing10_model.h5"
        # print("model dir",model_dir)
        model_loaded=audio_emotion.livePredictions()

        audio_file_path =path+"audioData"
        files = os.listdir(audio_file_path)
        final_emotions = {"neutral": 0, "calm": 0, "happy": 0, "sad": 0, "angry": 0, "fearful": 0, "disgust": 0, "surprised": 0}
        for file in files:
            emotions = model_loaded.makepredictions(audio_file_path+"\\"+file)
            final_emotions[emotions] += 1
        dir = "../Interviewer/media/audioData/"
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
        total = sum(final_emotions.values())
        average = total//len(final_emotions)
        maximum_diff = float("-inf")
        emotion = None
        for key in final_emotions:
            if abs(final_emotions[key] - average) > maximum_diff and final_emotions[key] > 0:
                maximum_diff = abs(final_emotions[key] - average)
                emotion = key
        audioEmotion = emotion

        analysis.analyze(data_queue.path)

        with open('result.json') as json_data:
            data = json.load(json_data)
        length = len(data)
        for key in data:
            # curr_user = request.user.username+str(i)
            face_emotion = data[key]
            max_diff = float("-inf")
            summ = sum(face_emotion.values())
            avg = summ//len(face_emotion)
            emt = None
            for i in face_emotion:
                if abs(face_emotion[i] - avg) > max_diff and face_emotion[i] > 0:
                    max_diff = abs(face_emotion[i] - avg)
                    emt = i

            profile_instance = Profile()
            profile_instance.user_id = request.user
            profile_instance.date = datetime.datetime.now()
            profile_instance.facial_expressions_keys = list(face_emotion.keys())
            profile_instance.facial_expressions_values = list(face_emotion.values())
            profile_instance.audio_analysis_keys = list(final_emotions.keys())
            profile_instance.audio_analysis_values = list(final_emotions.values())
            profile_instance.average_face_emotions = emt
            profile_instance.average_audio_emotions = audioEmotion
            profile_instance.save()
        # print(data_queue.path)

        return HttpResponse("Done")
    return render(request,'temp.html')

def profile(request):
    if request.user.is_authenticated:
        # data1 = Profile.objects.filter(user_id=request.user).last().facial_expressions_keys
        # data1 = data1.strip('][').split(', ')
        data2 = Profile.objects.filter(user_id=request.user).last().facial_expressions_values
        data2 = data2.strip('][').split(', ')
        data2 = list(map(int, data2))
        # data3 = Profile.objects.filter(user_id=request.user).last().audio_analysis_keys
        # data3 = data3.strip('][').split(', ')
        data4 = Profile.objects.filter(user_id=request.user).last().audio_analysis_values
        data4 = data4.strip('][').split(', ')
        data4 = list(map(int, data4))
        data5 = Profile.objects.filter(user_id=request.user).last().average_face_emotions
        data6 = Profile.objects.filter(user_id=request.user).last().average_audio_emotions
        data = Profile.objects.filter(user_id=request.user).order_by('id').reverse()
        return render(request,'profile.html', {'data2': data2, 'data4': data4, 'avg_face': data5, 'avg_audio': data6, 'data': data})
    return redirect('login')
'''
def gen(camera):
    i = 0
    while True:
        frame = camera.get_frame()[0]
        print(frame[1])
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        # if i== 10: #and i <80 :
            # break
            # cv2.imwrite(r'E:\Project\final_project_material\Interviewer\kang'+str(i)+'.jpg',frame[1])
        # cv2.imshow('Image',frame[1])
        # i+=1


def video_feed(request):
    return StreamingHttpResponse(gen(VideoCamera()),content_type='multipart/x-mixed-replace; boundary=frame')



def temp1(request):
    return render(request,'temp1.html')


'''




