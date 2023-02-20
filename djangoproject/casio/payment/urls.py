from django.urls import path
from . import views
app_name='payment'
urlpatterns = [
 path('', views.process_payment, name="initiate-payment"),
    #path('<str:ref>/', views.verify_payment, name="verify-payment"),
    path('callback', views.payment_response, name='payment_response'),
     path('cryptosuccess', views.cryptosuccess, name='cryptosuccess'),
          path('cryptoerror', views.cryptoerror, name='cryptoerror')
]