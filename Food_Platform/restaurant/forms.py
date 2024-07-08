from django import forms 
from .models import RestaurantRegistration
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

# class RestaurantSignup(forms.ModelForm):
#     class Meta:
#         model=Restaurant_Registration
#         fields=["Fullname","Email","Address","Password","Repeat_password"]


class RestaurantSignup(UserCreationForm):
    first_name=forms.CharField(required=True)
    last_name=forms.CharField(required=True)
    email=forms.EmailField(required=True)
    class Meta:
        model=User
        fields=["first_name","last_name","email","username"]

class AddRestaurant(forms.ModelForm):
    class Meta:
        model=RestaurantRegistration
        fields=['restaurant_name','image','location','cost_for_two']

class ShowRestaurantProfile(UserChangeForm):
    password=None
    class Meta:
        model=User  
        fields=["first_name","last_name","email","username"]

