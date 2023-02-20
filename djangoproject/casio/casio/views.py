from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from bet.models import UserProfile,Allbet
import datetime
from payment.models import Payment
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
    userprof= UserProfile.objects.get(email=request.user.username)
    todaydate = datetime.date.today()
    # confirm name of today
    todayname = datetime.datetime.today().strftime("%A")
    # let filter all with today first
    todayfilter = Allbet.objects.filter(date=todaydate)
    n = todaydate.strftime("%B")
    print("kkkkkk",todaydate.strftime("%B"),todaydate.year)
    if todayfilter.exists():
        todaydata={"today":todayfilter,"todayname":todayname,"month":n,"year":todaydate.year,"day":todaydate.day}
    else:
        todaydata=None
    return render(request,"pages/home.html",{"today":todaydata,"userprof":userprof})

@login_required
def draw(request):
    # check today date
    todaydate = datetime.date.today()
    # confirm name of today
    todayname = datetime.datetime.today().strftime("%A")
    # let filter all with today first
    todayfilter = Allbet.objects.filter(date=todaydate)
    n = todaydate.strftime("%B")
    print("kkkkkk",todaydate.strftime("%B"),todaydate.year)
    if todayfilter.exists():
        todaydata={"today":todayfilter,"todayname":todayname,"month":n,"year":todaydate.year,"day":todaydate.day}
    else:
        todaydata=None
    yesterdaydate=datetime.date.today() + datetime.timedelta(days=-1)
    yesfilter = Allbet.objects.filter(date=yesterdaydate)
    print(yesterdaydate.strftime("%A"))
    print(yesterdaydate.strftime("%B"))
    if yesfilter.exists():
        yesdata={"today":yesfilter,"todayname":yesterdaydate.strftime("%A"),"month":yesterdaydate.strftime("%B"),"year":yesterdaydate.year,"day":yesterdaydate.day}
    else:
        yesdata=None
    twodaydate=datetime.date.today() + datetime.timedelta(days=-2)
    twofilter = Allbet.objects.filter(date=twodaydate)
    if todayfilter.exists():
        twodata={"today":twofilter,"todayname":twodaydate.strftime("%A"),"month":twodaydate.strftime("%B"),"year":twodaydate.year,"day":yesterdaydate.day}
    else:
        twodata=None
    todayfilter = Allbet.objects.filter(date=todaydate)
    if todayfilter.exists():
        todaydata={"today":todayfilter,"todayname":todayname}
    return render(request,"pages/uncoming-draw.html",{"today":todaydata,"yesterday":yesdata,"twodayago":twodata})

@login_required
def profile(request):
    userprof= UserProfile.objects.get(email=request.user.username)
    
    return render(request,"pages/profile.html",{"userprof":userprof})
@login_required
def password(request):
    userprof= UserProfile.objects.get(email=request.user.username)
    
    return render(request,"pages/changepassword.html",{"userprof":userprof})

@login_required
def mail(request):
    userprof= UserProfile.objects.get(email=request.user.username)
    
    return render(request,"pages/changeemail.html",{"userprof":userprof})


@login_required
def notice(request):
    userprof= UserProfile.objects.get(email=request.user.username)
    
    return render(request,"pages/notifications.html",{"userprof":userprof})
@login_required
def withdraw(request):
    userprof= UserProfile.objects.get(email=request.user.username)
    
    return render(request,"pages/withdraw.html",{"userprof":userprof})
@login_required
def transaction(request):
    userprof= UserProfile.objects.get(email=request.user.username)
    trans = Payment.objects.filter(userprof=userprof)
    return render(request,"pages/transactions.html",{"userprof":userprof,"trans":trans})
@login_required
def setting(request):
    userprof= UserProfile.objects.get(email=request.user.username)
    
    return render(request,"pages/settings.html",{"userprof":userprof})
@login_required
def game(request):

    if request.method=="POST":
        print("ppoo")
        userprof= UserProfile.objects.get(email=request.user.username)
        betid = request.POST.get("betid")
        bet = Allbet.objects.get(id=betid)
        many = request.POST.get("method")
        amount = request.POST.get("total")
        return render(request,"pages/result.html",{"many":many,"amount":amount,"bet":bet,"userprof":userprof})
    else:
        userprof= UserProfile.objects.get(email=request.user.username)
        mo= request.GET.get("p")
        bet = Allbet.objects.get(id=mo)
    return render(request,"pages/game.html",{"userprof":userprof,"bet":bet})

@csrf_exempt
@login_required
def play(request):


    if request.method=="POST":
        print("ppoo")
        userprof= UserProfile.objects.get(email=request.user.username)
        betid = request.POST.get("betid")
        bet = Allbet.objects.get(id=betid)
        many = request.POST.get("method")
        amount = request.POST.get("total")
        return render(request,"pages/result.html",{"many":many,"amount":amount,"bet":bet,"userprof":userprof})
    return render(request,"pages/result.html",{"userprof":userprof,"bet":bet})
@csrf_exempt
@login_required
def editprofile(request):
    userprof= UserProfile.objects.get(email=request.user.username)
    if request.method=="POST":
        fullname = request.POST.get("fullname")
        phone = request.POST.get("phone")
        country = request.POST.get("country")
        state = request.POST.get("state")
        withdraw_pin = request.POST.get("withdraw")
        print(country)
        user = UserProfile.objects.get(email=request.user.username)
        user.phone=phone
        user.fullname=fullname
        user.country=country
        user.city = state
        user.withdraw_pin = withdraw_pin
        user.save()
        return render(request,"pages/profile.html",{"userprof":userprof})
    return render(request,"pages/editprofile.html",{"userprof":userprof})

    
def logout_view(request):
    logout(request)
    return login_view(request)

