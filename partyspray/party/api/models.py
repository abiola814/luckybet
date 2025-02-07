from django.contrib.auth.models import User

# Create your models here.
# from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db.models import Q
import random
import os
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, phone,email,username=None, password=None, is_staff=False, is_active=True, is_admin=False):
        if not phone:
            raise ValueError('user must have a phone number')
        if not email:
            raise ValueError('user must have a email')

        if not password:
            raise ValueError('user must have a password')
        user_obj = self.model(
            email=self.normalize_email(email),
            phone=phone,
            username=username
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj
    def create_main_user(self, email, password=None, is_staff=True, is_active=True, is_admin=True):
        if not email:
            raise ValueError('users must have a phone number')
        if not password:
            raise ValueError('user must have a password')

        user_obj = self.model(
            email=email
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, phone, password=None):
        user = self.create_main_user(
            phone,
            password=password,
            is_staff=True,


        )
        return user

    def create_superuser(self, email, password=None):
        user = self.create_main_user(
            email,
            password=password,
            is_staff=True,
            is_admin=True,


        )
        return user

def upload_image_path_profile(instance, filename):
    new_filename = random.randint(1,9996666666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "profile/{new_filename}/{final_filename}".format(
            new_filename=new_filename,
            final_filename=final_filename
    )
         

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

class User(AbstractBaseUser):
    phone_regex      = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone            = models.CharField(validators=[phone_regex], max_length=17,unique=True)
    name             = models.CharField(max_length = 20, blank = True, null = True)
    cc_number             = models.IntegerField(blank = True, null = True)
    cc_cvv             = models.IntegerField(blank = True, null = True)
    cc_expiry             = models.IntegerField(blank = True, null = True)
    username         = models.CharField(max_length = 80, blank = True, null = True)
    recoveryCode     = models.CharField(max_length = 6, blank = True, null = True)
    avatar               =   models.ImageField(upload_to = upload_image_path_profile, default=None, null = True, blank = True)
    email            = models.EmailField(unique=True)
    first_login      = models.BooleanField(default=False)
    active           = models.BooleanField(default=True)
    staff            = models.BooleanField(default=False)
    admin            = models.BooleanField(default=False)
    timestamp        = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.name
    def get_email(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):

        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
    

