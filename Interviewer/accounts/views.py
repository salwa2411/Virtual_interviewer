from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm

from django.http.response import StreamingHttpResponse
from accounts.camera import VideoCamera
import cv2

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
<<<<<<< HEAD
        questions = ["Tell me About Yourself", "Why should we hire you?", "What is your strength and weakness?"]
=======
        questions = ["Tell me About Yourself", "Why should we hire you?", "What are your strengths and weaknesses?"]
>>>>>>> f0a18aac2891e012ad2ca09c1f5d2e369deeb08c
        return render(request,'interview.html', {'questions': questions})
    return redirect('login')


# def takeInterview(request):
#     if request.user.is_authenticated:
#         return render(request,'interview.html')
#     return redirect('login')

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

def temp(request):


    return render(request,'temp.html')

def temp1(request):
    return render(request,'temp1.html')


'''




