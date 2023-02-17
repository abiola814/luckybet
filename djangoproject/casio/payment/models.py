from django.db import models
from django.urls import reverse
import secrets
from .paystack import PayStack
from bet.models import UserProfile
# Create your models here.

class Payment(models.Model):
    userprof= models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    email = models.EmailField()
    ref = models.CharField(max_length=200)
    method = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date_created",)

    def __str__(self) -> str:
        return f"{self.amount}"

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(10)
            object_with_similar_ref = Payment.objects.filter(ref=ref).first()
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def amount_value(self):
        return self.amount *100

    
    def verify_payment(self):
        if self.method == "transfer" or self.method == "ussd":
                
            paystack = PayStack()
            status, result = paystack.verify_payment(self.ref, self.amount)
            if status:
                self.paystack_response = result
                if result["amount"] == self.amount:
                    self.completed = True
                self.save()
                return True
            return False
