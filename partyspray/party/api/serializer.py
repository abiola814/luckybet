from rest_framework import serializers
from .models import User
from rest_framework.validators import ValidationError


# class ChangeSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(min_length=8,write_only=True)

#     class Meta:
#         model = User
#         fields= ["email","password"]
#     def validate(self,attrs):
#         check_password = User.objects.filter(email= attrs["password"]).exists()

#         if check_password:
#             raise ValidationError("Email has already been used")
        
#         return super().validate(attrs)

class UserSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = ('id', 'name','username','email','phone','cc_number','cc_expiry','cc_cvv',"avatar"
                  )
        #extra_kwargs = {'password': {'write_only': True}}