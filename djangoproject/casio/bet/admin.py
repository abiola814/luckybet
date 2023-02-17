from django.contrib import admin
from .models import UserProfile,winners,Allbet
# Register your models here.
admin.site.register(Allbet)
admin.site.register(UserProfile)
admin.site.register(winners)