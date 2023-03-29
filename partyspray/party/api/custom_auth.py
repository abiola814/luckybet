from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        UserModel = get_user_model()
        try:
            data = kwargs.get('email', None)
            # print("lllllllllllllllllllllll")
            if data is None:
                
                data = kwargs.get('phone', None)
                # print("tttttttttttttttttuuuuuuuuuuuuuuuuuu",data)
                user = UserModel.objects.get(phone=data)
            else:
                # print("oooooooooooooooooooooooooo")
                user = UserModel.objects.get(email=data)
            if user.check_password(kwargs.get('password', None)):
                return user
        except UserModel.DoesNotExist:
            return None
        return None