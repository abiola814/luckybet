from django.shortcuts import get_object_or_404, render, redirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from .models import Payment
from bet.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import math
import requests
import random

# def initiate_payment(request: HttpRequest) -> HttpResponse:
#     if request.method == "POST":
#         name= request.POST.get('name')
#         email = request.user.email
#         amount= 100
#         fee_type= request.POST.get('fee')
#         state_ID= request.POST.get('state')
#         pay = Payment.objects.create(name=name,email=email,amount=amount,fee_type=fee_type,state_ID=state_ID)
#         # pays = Payment.objects.get(ref=pay.ref)
#         return JsonResponse({'payment': pay, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})

#     return render(request, "connector.html")

#@login_required
# def initiate_payment(request):
#     if request.method == "POST":
#         amount= request.POST.get('amount')
#         typ= request.POST.get('method')

#         email = request.user.username
#         userprof= UserProfile.objects.get(email = email)
#         pay = Payment.objects.create(userprof=userprof,email=email,amount=amount,method=typ)
#         # pays = Payment.objects.get(ref=pay.ref)
    
#         return render(request,"pages/confirmpay.html",{'payment': pay, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
#     return render(request,"pages/fund.html")

def verify_payment(request, ref: str):
    trxref = request.GET["trxref"]
    if trxref != ref:
        messages.error(
            request,
            "The transaction reference passed was different from the actual reference. Please do not modify data during transactions",
        )
    payment: Payment = get_object_or_404(Payment, ref=ref)
    if payment.verify_payment():
        messages.success(
            request, f"Payment Completed Successfully, usd #{payment.amount}."
        )
  
    else:
        messages.warning(request, "Sorry, your payment could not be confirmed.")
    return render(request, "pages/fund.html")
def process_payment(request):
    userprof= UserProfile.objects.get(email = request.user.username)
    amount= request.POST.get('amount')
    
    hed = {'Authorization': 'Bearer ' + "FLWSECK_TEST-e3a50c9e6203cc6c1b564bdd0589dfd5-X"}
    data = {
            "tx_ref":''+str(math.floor(1000000 + random.random()*9000000)),
            "amount":amount,
            "currency":"USD",
            "redirect_url":"http://localhost:8000/fund/callback",
            "payment_options":"card",
            "meta":{
                "consumer_id":100212510,
                "consumer_mac":"92a3-912ba-1192a"
            },
            "customer":{
                "email":userprof.email,
                "phonenumber":userprof.phone,
                "name":userprof.fullnamename
            },
            "customizations":{
                "title":"lottery",
                "description":"Best store in town",
                "logo":"https://getbootstrap.com/docs/4.0/assets/brand/bootstrap-solid.svg"
            }
            }
    url = ' https://api.flutterwave.com/v3/payments'
    response = requests.post(url, json=data, headers=hed)
    response=response.json()
    link=response['data']['link']
    return link

from django.views.decorators.http import require_http_methods
from django.http import HttpResponse


@require_http_methods(['GET', 'POST'])
def payment_response(request):
    status=request.GET.get('status', None)
    tx_ref=request.GET.get('tx_ref', None)
    print(status)
    print(tx_ref)
    return HttpResponse('Finished')