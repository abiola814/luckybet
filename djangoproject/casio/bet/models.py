from django.db import models

# Create your models here.

# create user profile for developer

class UserProfile(models.Model):
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=25 )
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.name}"