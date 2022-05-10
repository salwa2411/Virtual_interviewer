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
from .tasks import anas

from . import analysis
from . import data_queue
from . import audio_analysis
from . import audio_emotion
from accounts.models import Profile
import datetime
# from pathlib import Path
import os.path

counter = 0
def home(request):
    if not os.path.exists('../Interviewer/media'):
        os.mkdir("../Interviewer/media")
        os.mkdir("../Interviewer/media/audioData")
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
    # global audioEmotion
    global counter
    counter+=1
    path = os.getcwd() +r"/media/"
    username = request.user.username
    userid = request.user.id
    if request.method == 'POST':
        print(request.body)

        with open(f"{path}"+f"{username}" + str(counter) + ".mp4", "wb") as test:
            test.write(request.body)

        anas.delay(username, counter, path, userid)
        return HttpResponse("Done")
    return render(request,'temp.html')

def profile(request):
    if request.user.is_authenticated:
        data2 = Profile.objects.filter(user_id=request.user).last().facial_expressions_values
        data2 = data2.strip('][').split(', ')
        data2 = list(map(int, data2))
        data4 = Profile.objects.filter(user_id=request.user).last().audio_analysis_values
        data4 = data4.strip('][').split(', ')
        data4 = list(map(int, data4))
        data5 = Profile.objects.filter(user_id=request.user).last().average_face_emotions
        data6 = Profile.objects.filter(user_id=request.user).last().average_audio_emotions
        data = Profile.objects.filter(user_id=request.user).order_by('id').reverse()
        return render(request,'profile.html', {'data2': data2, 'data4': data4, 'avg_face': data5, 'avg_audio': data6, 'data': data})
    return redirect('login')
