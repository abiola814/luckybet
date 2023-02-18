from django.urls import path
from . import views

urlpatterns = [
 #   path('', views.initiate_payment, name="initiate-payment"),
    path('addbet/', views.addbet, name="addbet"),
]