from django.db import models

# Create your models here.

# create user profile for developer

class UserProfile(models.Model):
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=25 )
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    withdraw_pin = models.CharField(max_length=100)
    amount = models.IntegerField(default=0)
    totalwin = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.fullname}"


class winners(models.Model):
    bet = models.CharField(max_length=10)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    win = models.BooleanField(default=False)
    number = models.IntegerField(default=0)
    numbe2 = models.IntegerField(default=0)
    numbe3 = models.IntegerField(default=0)
    

    # class Meta:
    #     verbose_name = _("")
    #     verbose_name_plural = _("s")

    def __str__(self):
        return self.user

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})

class Allbet(models.Model):
    number1= models.IntegerField()
    number2= models.IntegerField()
    number3= models.IntegerField()
    number4= models.IntegerField()
    number5= models.IntegerField()
    totalpot=  models.IntegerField(default=0)
    winning_one= models.IntegerField()
    winning_two= models.IntegerField()
    date = models.DateField( auto_now=True)
    time=models.TimeField( auto_now=True)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.winning_one} {self.winning_two}"



