from django.contrib import admin
from .models import Customer_Profile
# Register your models here.

@admin.register(Customer_Profile)
class CustomerAdmin(admin.ModelAdmin):
    list_display=["User","User_Photo","Address","contact_no"]


# admin.site.register(Customer_Registration)