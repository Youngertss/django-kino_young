from django.contrib import admin
from .models import *
# Register your models here.

class AdminUser(admin.ModelAdmin):
    fields = ["username", "money", "is_support"]

admin.site.register(KinoUsers, AdminUser)