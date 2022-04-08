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
        final_emotions = {}
        for file in files:
            emotions = model_loaded.makepredictions(audio_file_path+"\\"+file)
            if emotions in final_emotions:
                final_emotions[emotions] += 1
            else:
                final_emotions[emotions] = 1
        dir = "../Interviewer/media/audioData/"
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
        total = sum(final_emotions.values())
        average = total//len(final_emotions)
        minimum_diff = float("inf")
        emotion = emotions
        for key in final_emotions:
            if abs(final_emotions[key] - average) < minimum_diff:
                minimum_diff = abs(final_emotions[key] - average)
                emotion = key
        audioEmotion = emotion

        analysis.analyze(data_queue.path)

        with open('result.json') as json_data:
            data = json.load(json_data)
        length = len(data)
        for i in range(1, length+1):
            curr_user = request.user.username+str(i)
            face_emotion = data[curr_user]
            min_diff = float("inf")
            summ = sum(face_emotion.values())
            avg = summ//len(face_emotion)
            emt = None
            for i in face_emotion:
                if abs(face_emotion[i] - avg) < min_diff:
                    min_diff = abs(face_emotion[i] - avg)
                    emt = i


            profile_instance = Profile()
            profile_instance.user_id = request.user
            profile_instance.date = datetime.datetime.now()
            profile_instance.facial_expressions = emt
            profile_instance.audio_analysis = audioEmotion
            profile_instance.accuracy = "98"
            profile_instance.save()
        # print(data_queue.path)

        return HttpResponse("Done")
    return render(request,'temp.html')

def profile(request):
    if request.user.is_authenticated:
        context = {
        'data': Profile.objects.filter(user_id=request.user)
        }
        return render(request,'profile.html', context)
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




