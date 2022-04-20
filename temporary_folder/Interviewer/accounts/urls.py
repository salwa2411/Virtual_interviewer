from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name="home"),
    path('accounts/register',views.registerUser, name="register"),
    path('accounts/login',views.loginUser,name="login"),
    path('accounts/logout/', views.logoutUser, name="logout"),
    path('interview/',views.takeInterview,name='interview'),
    path('profile/',views.profile,name="profile"),
    path('temp/',views.temp,name= "temp")
]
