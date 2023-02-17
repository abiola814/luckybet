from django.db import models

# Create your models here.

# create user profile for developer

class UserProfile(models.Model):
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=25 )
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.fullname}"


class winners(models.Model):
    bet = models.CharField(max_length=10)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    win = models.BooleanField()
    number = models.CharField(max_length=10)

    

    # class Meta:
    #     verbose_name = _("")
    #     verbose_name_plural = _("s")

    def __str__(self):
        return self.user

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})

class Allbet(models.Model):
    number1= models.IntegerField(max_length=2)
    number2= models.IntegerField(max_length=2)
    number3= models.IntegerField(max_length=2)
    number4= models.IntegerField(max_length=2)
    number5= models.IntegerField(max_length=2)
    totalpot=  models.IntegerField(max_length=100)
    winning_one= models.IntegerField(max_length=2)
    winning_two= models.IntegerField(max_length=2)
    date = models.DateField( auto_now=False, auto_now_add=False)
    time=models.TimeField( auto_now=False, auto_now_add=False)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.date



