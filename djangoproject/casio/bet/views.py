from django.shortcuts import render
from . models import Allbet
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def addbet(request):

    p= [request.POST.get("kk"),request.POST.get("rr"),request.POST.get("k"),request.POST.get("kkk"),request.POST.get("val")]
    o=[request.POST.get("e"),request.POST.get("ee")]
    print("oooooooooooo",p)
    j=o[0]
    n=o[1]
    win1= p[int(o[0])]
    win2 = p[int(o[1])]
    Allbet(number1=p[0],number2=p[1],number3=p[2],
    number4=p[3],number5=p[4],winning_one=win1,winning_two=win2).save()
    return True