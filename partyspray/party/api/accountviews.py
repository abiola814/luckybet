from rest_framework.views import APIView
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.request import Request
# from django.contrib.auth import authenticate
from .jwt_token import create_jwt_for_user
from rest_framework.permissions import IsAuthenticated
from django.db.models.query_utils import Q
from django.template.loader import render_to_string
import secrets
from django.core.mail import send_mail, BadHeaderError
from .custom_auth import CustomAuthBackend

from .models import User
# Create your views here.

class SignupView(generics.GenericAPIView):
    
    permission_classes=[]
    def post(self,request:Request):
        data = request.data
        username= data.get("username")
        password = data.get("password")
        email = data.get('email')
        phone = data.get('phone')
        verify_phone = User.objects.filter(phone=phone).exists()
        verify_email = User.objects.filter(email=email).exists()
        verify_username = User.objects.filter(username=username).exists()
        if verify_email:
            response ={ "requestType":"outbound",
                        "message": "Sorry, email has been used",
                        "status":False
                        }
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)
        if verify_username:
            response ={ "requestType":"outbound",
                        "message":"Sorry, username has been used",
                        "status":False
                        }
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)


        try:        
            User.objects.create_user(username=username,email=email,phone=phone,password=password)

        except ValueError as error:
            response ={ "requestType":"outbound", 
                        "message":str(error),
                        "status":False
                        }
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)
        response ={ "requestType":"outbound",
        "message":"user successfully created",
        "status":True
        }
        return Response(data=response,status=status.HTTP_201_CREATED)
        # return Response(data=response,status=status.HTTP_201_CREATED)
        
class LoginView(APIView):
    permission_classes=[]
    def post(self,request:Request):
    
        phone = request.data.get("phone",None)
        email = request.data.get("email",None)
        # print(User.objects.get(phone=phone))
        password = request.data.get("password",None)
        if email is None:
            if phone is None:
                response ={ "requesttype":"outbound",
                "message":"Please, input an email",
                "status":False,
                }
                return Response(data=response,status=status.HTTP_400_BAD_REQUEST)
        if password is None:
            response ={ "requesttype":"outbound",
            "message":"Please, input a password",
            "status":False,
            }
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)
        print(email,password)
        user = CustomAuthBackend.authenticate(self,request,email=email,phone=phone,password=password)
        print(user)
        if user is not None:
            tokens = create_jwt_for_user(user)
            response = {
                "status":True,
                "message":"login successfull",
                "token":tokens
            }
            return Response(data=response,status=status.HTTP_201_CREATED)
        else:
            response ={ "requesttype":"outbound",
                "message":"unable to verify user credential",
                "status":False,
            }
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)

    # def get(self,request:Request):
    #     content={
    #         "user":str(request.user),
    #         "auth":str(request.auth)
    #     }
    #     return Response(data=content,status=status.HTTP_200_OK)
    # 
class ForgotPasswordView(generics.GenericAPIView):
    
    permission_classes=[]
    def post(self,request:Request):
        data = request.data
        email= data.get("email")
        if email:
            associated_users = User.objects.filter(Q(email=email))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    code = "po788"
                    user.code=code
                    c = {
                    "email":user.username,
                    'domain':'localhost',
                    'site_name': 'Website',
                    "user": user,
                    'protocol': 'http',
                    'code':code,
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'help@casioluckybet.live' , [user.email], fail_silently=False)
                        response ={ 
                                "requesttype":"outbound",
                                "message":f"Please, email has been sent to {user.email}",
                                "status":True,
                                        }
                    except BadHeaderError:
                        response ={ 
                            "requesttype":"outbound",
                            "message":"unable to verify user credential",
                            "status":False,
                                    }
                        return Response(data=response,status=status.HTTP_400_BAD_REQUEST)
                    return Response(data=response,status=status.HTTP_201_CREATED)
                    
            else:
                response ={ 
                    "requesttype":"outbound",
                    "message":"Sorry, email is not asssociated to any account",
                    "status":False,
                            }
                return Response(data=response,status=status.HTTP_400_BAD_REQUEST)                  
        else:
            response ={ 
                "requesttype":"outbound",
                "message":"please enter a email in the input",
                "status":False,
                        }
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)
    def put(self,request:Request):
        pass

        