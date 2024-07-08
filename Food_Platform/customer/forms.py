from django import forms 
from .models import Customer_Profile

from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

class CustomerSignup(UserCreationForm):
    first_name=forms.CharField(required=True)
    last_name=forms.CharField(required=True)
    email=forms.EmailField(required=True)
    class Meta:
        model=User
        fields=["first_name","last_name","email","username"]

class ShowRestaurantProfile(UserChangeForm):
    password=None
    class Meta:
        model=User  
        fields=["first_name","last_name","email","username"]

class CustomerDetails(forms.ModelForm):
    class Meta:
        model=Customer_Profile
        fields=["User_Photo","Address","contact_no"]

