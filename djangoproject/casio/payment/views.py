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

@login_required
def initiate_payment(request):
 
    return render(request,"pages/fund.html")

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
    if request.method == "POST":
        userprof= UserProfile.objects.get(email = request.user.username)
        amount= request.POST.get('amount')
        method= request.POST.get('method')

        print(method)
        if method == "crypto":
            txid=str(math.floor(1000000 + random.random()*9000000))
            hed = {'x-api-key':"ZW4KKVG-PAWM5DG-N93YQGY-56Y9G16"}
            data = {
                   "price_amount": amount,
                    "price_currency": "usd",
                    "order_id": txid,
                    "order_description": "Apple Macbook Pro 2019 x 1",
                    "ipn_callback_url": "https://nowpayments.io",
                    "success_url": "http://localhost:8000/fund/cryptosuccess",
                    "cancel_url": "http://localhost:8000/fund/cryptocancelled"
                    }
            url = 'https://api-sandbox.nowpayments.io/v1/invoice'
            response = requests.post(url, json=data, headers=hed)
            response=response.json()
            print(response)
            link=response['invoice_url']
            Payment(userprof=userprof,txid=txid,method=method,amount=amount).save()
            print(link)
            return JsonResponse({'status': "success", 'link': link})
        else:
            txid=str(math.floor(1000000 + random.random()*9000000))
            hed = {'Authorization': 'Bearer ' + "FLWSECK_TEST-e3a50c9e6203cc6c1b564bdd0589dfd5-X"}
            data = {
                    "tx_ref":''+ txid,
                    "amount":amount,
                    "currency":"NGN",
                    "redirect_url":"http://localhost:8000/fund/callback",

                    "payment_options": "card, banktransfer, ussd",
                    "meta":{
                        "consumer_id":23,
                        "consumer_mac":"92a3-912ba-1192a"
                    },
                    "customer":{
                        "email":userprof.email,
                        "phonenumber":userprof.phone,
                        "name":userprof.fullname
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
            Payment(userprof=userprof,txid=txid,method=method,amount=amount,typ="deposit").save()
            print(link)
            return JsonResponse({'status': "success", 'link': link})
    return render(request, "pages/fund.html")

from django.views.decorators.http import require_http_methods
from django.http import HttpResponse


@require_http_methods(['GET', 'POST'])
def payment_response(request):
    status=request.GET.get('status', None)
    tx_ref=request.GET.get('tx_ref', None)
    pay= Payment.objects.get(txid=tx_ref)
    print(pay)
    user= UserProfile.objects.get(email=request.user.username)
    if status=="success":
        pay.verified=True
        pay.status= status
        pay.save()
        user.amount += int(pay.amount)
        user.save()
        messages.success(
            request, f"Payment Completed Successfully, usd {pay.amount}."
        )
    else:
        pay.verified=True
        pay.status= status
        pay.save()
        messages.warning(
            request, f"Payment  {status}, usd {pay.amount}."
        )     
    print(status)
    print(tx_ref)

    return render(request, "pages/fund.html")

def cryptosuccess(request):
    id=request.GET.get('NP_id', None)
    print("eeeeeeeeeeeeeeeeeeeeeee",id)
    url = 'https://api-sandbox.nowpayments.io/v1/payment/'+ id
    hed = {'x-api-key':"ZW4KKVG-PAWM5DG-N93YQGY-56Y9G16"}
    print("eeeeeeeeeeeeeeeeeeeeeee",url)
    response = requests.get(url,headers=hed)
    response=response.json()
    print(response)
    order=response['order_id']
    user= UserProfile.objects.get(email=request.user.username)
    pay= Payment.objects.get(txid=order) 
    pay.verified=True
    pay.status= "success"
    pay.save()
    user.amount += int(pay.amount)
    user.save() 
    messages.success(
        request, f"Payment Completed Successfully, usd ."
    )   
    return render(request, "pages/fund.html")

def cryptoerror(request):
    id=request.GET.get('NP_id')
    print("eeeeeeeeeeeeeeeeeeeeeee",id)
    url = 'https://api-sandbox.nowpayments.io/v1/invoice/'+ id
    response = requests.get(url)
    response=response.json()
    print("jjjjjjjjjjjjjjjjjjjjjjj",response)
    order=response['order_id']
    user= UserProfile.objects.get(email=request.user.username)
    pay= Payment.objects.get(txid=order) 
    pay.verified=True
    pay.status= "cancelled"
    pay.save() 
    messages.success(
        request, f" Crypto Payment Cancelled ."
    )   
    return render(request, "pages/fund.html")