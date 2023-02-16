from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from bet.models import UserProfile

@csrf_exempt
def landingpage(request):
    if request.method=="POST":
        password = request.POST.get("password")
        fullname = request.POST.get("fullname")

        email = request.POST.get("email")
        phone = request.POST.get("phone")
        print(password,email,fullname,phone)
        username=email
        r = User.objects.filter(username=email)
        if r.exists():
            return JsonResponse({"status": 'email already associated with another account'})  
        User.objects.create_user(username=username,password=password)
        UserProfile(email=email,phone=phone,fullname=fullname).save()
        user = authenticate(username=email, password=password)
        login(request,user)
        return JsonResponse({"status": 'Success'})       
    return render(request,"index.html")

def login_view(request):
    if request.method=="POST":
        password = request.POST.get("password")
        email = request.POST.get("email")
        user = authenticate(username=email, password=password)
        if user is None:
            return JsonResponse({"status": 'invalid credential'})            
        login(request, user)
        return JsonResponse({"status": 'Success'})    
    return render(request,"pages/login.html")    

@login_required
def home(request):
    return render(request,"pages/home.html")

@login_required
def draw(request):
    return render(request,"pages/uncoming-draw.html")

@login_required
def profile(request):
    userprof= UserProfile.objects.get(email=request.user.username)
    
    return render(request,"pages/profile.html",{"userprof":userprof})

@login_required
def fund(request):
    return render(request,"pages/fund.html")
    
def logout_view(request):
    logout(request)
    return login_view(request)

