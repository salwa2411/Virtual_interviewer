from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('accounts/register',views.registerUser, name="register"),
    path('accounts/login',views.loginUser,name="login"),
    path('accounts/logout/', views.logoutUser, name="logout"),
    path('interview/',views.takeInterview,name='interview'),
    # path('video_feed', views.video_feed, name='video_feed'),
    # path('temp/',views.temp,name= "temp"),
    # path('temp1/',views.temp1,name="temp1"),
]
