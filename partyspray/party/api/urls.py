from django.contrib import admin
from django.urls import path,include
from .accountviews import SignupView,LoginView,ForgotPasswordView
from .userview import changepassword,changePhoto,AddCard,Profile

urlpatterns = [

    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='loginup'),
    path('forgotpassword/',ForgotPasswordView.as_view()),
    path('changepassword/', changepassword.as_view(), name='changepassword'),
    path('changeimage/', changePhoto.as_view(), name='changephoto'),
    path("profile/",Profile.as_view())
]
