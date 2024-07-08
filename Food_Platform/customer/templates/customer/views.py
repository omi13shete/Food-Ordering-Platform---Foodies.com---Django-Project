from django.shortcuts import render
from .forms import CustomerSignup
from django.shortcuts import render,HttpResponseRedirect
from .forms import RestaurantSignup,ShowRestaurantProfile
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout
# Create your views here.

# CRUD OPERATIONS

# To create customer account

def customer_signup(request):
    if request.method == "POST":
        fm=CustomerSignup(request.POST)
        if fm.is_valid():
            fm.save()
            print("task done")
            return render(request,"core/home.html")
    else:
        fm=CustomerSignup()
    return render(request,"restaurant/restaurant_signup.html",{"forms":fm})



# CUSTOMER LOGIN 
def customer_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        if request.method == "POST":
            fm=AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                uname=fm.cleaned_data["username"]
                upass=fm.cleaned_data["password"]
                user=authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    return HttpResponseRedirect("/")
                else:
                    return render(request,"customer/customer_login.html")
        else:
            fm=AuthenticationForm()
    
    return render(request,"customer/customer_login.html",{"login_form":fm})



# CUSTOMER LOGOUT
def customer_logout(request):
    logout(request)
    return HttpResponseRedirect("/customer/restaurant_login/")



# CUSTOMER PROFILE
def customer_profile(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            fm=ShowRestaurantProfile(request.POST,instance=request.user)
            if fm.is_valid():
                fm.save()
        else:
            fm=ShowRestaurantProfile(instance=request.user)
        return render(request,"customer/customer_profile.html",{"name":request.user,"form":fm})
    else:
        return HttpResponseRedirect("/customer/customer_login/")
    



# CHANGE PASSWORD
def customer_change_pass(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            fm=PasswordChangeForm(user=request.user,data=request.POST)
            if fm.is_valid():
                fm.save()
                return HttpResponseRedirect("/customer/restaurant_profile/")
        else:
            fm=PasswordChangeForm(request)
        return render(request,"customer/change_password.html",{"change_pass_form":fm})
    else:
        return HttpResponseRedirect("/")

        




# 
