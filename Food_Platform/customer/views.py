from django.shortcuts import render
from .forms import CustomerSignup
from django.shortcuts import render,HttpResponseRedirect,redirect
from .forms import CustomerSignup,ShowRestaurantProfile,CustomerDetails
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout
from .models import Customer_Profile
# Create your views here.

# CRUD OPERATIONS

# To create customer account
def customer_signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        if request.method == "POST":
            fm=CustomerSignup(request.POST)
            if fm.is_valid():
                uname=fm.cleaned_data["username"]
                print("uname:",uname)
                upass=fm.cleaned_data["password1"]
                fm.save()
                user=authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    return HttpResponseRedirect("/customer/add_customer_details/")
                else:
                    return render(request,"customer/customer_signup.html")
        else:
            fm=CustomerSignup()
        return render(request,"customer/customer_signup.html",{"forms":fm})


        



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


def add_customer_details(request):
    if request.method== "POST":
        fm=CustomerDetails(request.POST , request.FILES)
        if fm.is_valid():
            customer=fm.save(commit=False)
            customer.User=request.user
            customer.save()
            print(customer)
            return redirect("show_customer_details" ,pk=customer.id)
    else:
        fm=CustomerDetails()
    return render(request,"customer/add_customer_details.html",{"form":fm})


def show_customer_details(request,pk):
    customer=Customer_Profile.objects.get(pk=pk)
    if request.method == "POST":
        fm=CustomerDetails(request.POST,request.FILES,instance=customer)
        if fm.is_valid():
            fm.save()
            return HttpResponseRedirect("/")
    else:
        fm=CustomerDetails(instance=customer)
    return render(request,"customer/show_customer_details.html",{"form":fm})


def delete_customer_details(request,pk):
    fm=Customer_Profile.objects.get(pk=pk)
    fm.delete()
    return render(request,"core/home.html")




