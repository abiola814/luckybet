from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializer import UserSerializer

class changepassword(generics.GenericAPIView):
    permission_classes=[IsAuthenticated]
    
    def post(self,request:Request):
        old_password = request.data.get("oldPassword",None)
        new_password = request.data.get("newPassword",None)
        confirm_password = request.data.get("confirmPassword",None)
        if old_password is None:
            response ={ "requestType":"outbound",
                        "message": "Please , input your old password",
                        "status":False
                        }
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)
        if new_password is None:
            response ={ "requestType":"outbound",
                        "message": "Please , input your new password",
                        "status":False
                        }
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)
        if confirm_password is None:
            response ={ "requestType":"outbound",
                        "message": "Please , input your confirm password",
                        "status":False
                        }
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)
        if confirm_password != new_password:
            response ={ "requestType":"outbound",
                        "message": "Sorry , your confirm password and new password did not match",
                        "status":False
                        }
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(email=request.user.email)
        checkPassword =user.check_password(old_password)
        if not checkPassword:
            response ={ "requestType":"outbound",
                        "message": "Sorry , incorrect old password",
                        "status":False
                        }
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)
        else:
            user.set_password(confirm_password)
            user.save()        
            response ={ "requestType":"outbound",
                        "message": "Password changed successfully",
                        "status":True
                        }
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)
class AddCard(generics.GenericAPIView):
    permission_classes=[IsAuthenticated]
    
    def post(self,request:Request):
        cc_number = request.data.get("cc_number",None)
        cc_expiryDate = request.data.get("cc_expiryDate",None)
        cc_code = request.data.get("cvv",None)
        if cc_code is None:
            response ={ "requestType":"outbound",
                        "message": "Sorry, fill in the cvv input",
                        "status":False
                        }
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)
        if cc_expiryDate is None:
            response ={ "requestType":"outbound",
                        "message": "Please, fill in the card expiry date",
                        "status":False
                        }
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)
        if cc_code is None:
            response ={ "requestType":"outbound",
                        "message": "please, fill in your card number",
                        "status":False
                        }
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(email=request.user.email)
        user.cc_number=cc_number
        user.cc_code = cc_code
        user.cc_expiry= cc_expiryDate
        user.save()
        response ={ "requestType":"outbound",
                        "message": "Successfully created",
                        "status":False
                        }
        return Response(data=response,status=status.HTTP_400_BAD_REQUEST)
    def patch(self,request:Request):
        cc_number = request.data.get("cc_number",None)
        cc_expiryDate = request.data.get("cc_expiryDate",None)
        cc_code = request.data.get("cvv",None)
        user = User.objects.get(email=request.user.email)
        if cc_code:
            user.cc_code=cc_code
        if cc_expiryDate :
            user.cc_expiry=cc_expiryDate
        if cc_number:
            user.cc_number = cc_number
        user.cc_number=cc_number
        user.cc_code = cc_code
        user.cc_expiry= cc_expiryDate
        user.save()
        response ={ "requestType":"outbound",
                        "message": "Card successfully updated ",
                        "status":False
                        }
        return Response(data=response,status=status.HTTP_400_BAD_REQUEST)
    def get(self,request:Request):
        try:
            user = User.objects.get(email=request.user.email)
        except:
            response ={ "requestType":"outbound",
                            "message": "Unable to retrieve user card details ",
                            "status":False
                            }
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)
        response ={ "requestType":"outbound",
                        "message": "successfully proccessed",
                        "status":True,
                        "data":{
                                "card": {
                                    "cc_number":user.cc_number,
                                    "cvv":user.cc_code,
                                    "cc_expiry":user.cc_expiry
                                }
                        }
                        }
        return Response(data=response,status=status.HTTP_400_BAD_REQUEST)       
        
class changePhoto(generics.GenericAPIView):
    permission_classes=[IsAuthenticated]

    def patch(self,request:Request):
        image = request.FILES.get('image',False)
        try:
            user = User.objects.get(email=request.user.email)
        except:
            response ={ "requestType":"outbound",
                            "message": "Unable to retrieve user card details ",
                            "status":False
                            }
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)
        if not image:
            response ={ "requestType":"outbound",
                            "message": "unable to update image please check the image selected ",
                            "status":False
                            }
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)
        user.avatar=image
        user.save()
        response ={ "requestType":"outbound",
                        "message": "Image uploaded successfully ",
                        "status":True
                        }
        return Response(data=response,status=status.HTTP_400_BAD_REQUEST)
    def get(self,request:Request):
        try:
            user = User.objects.get(email=request.user.email)
        except:
            response ={ "requestType":"outbound",
                            "message": "Unable to retrieve user card details ",
                            "status":False
                            }
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)
        try:
            image= user.avatar.url
        except ValueError:
            response ={ "requestType":"outbound",
                            "message": "No image available",
                            "status":False
                            }
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)
        response ={ "requestType":"outbound",
                        "message": "successfully proccessed",
                        "status":True,
                        "data":{
                                "user": {
                                    "image":image,
                                }
                        }
                        }
        return Response(data=response,status=status.HTTP_400_BAD_REQUEST)     

class Profile(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that 
        # can be JSONified and sent to the client. 
        serializer = self.serializer_class(request.user)
        response ={ "requestType":"outbound",
                        "message": "successfully proccessed",
                        "status":True,
                        "data":{
                                "user": serializer.data
                        }
                        }
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request, *args, **kwargs):
        username = request.data.get("username",None)
        phone = request.data.get("phone",None)
        name= request.data.get("name",None)
        email= request.data.get("email",None)

        temp_data = {'username':username,"phone":phone,"name":name,"email":email} 
        serializer_data=temp_data
        serializer = UserSerializer(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)