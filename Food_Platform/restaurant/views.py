from django.shortcuts import render,HttpResponseRedirect,redirect
from .forms import RestaurantSignup,ShowRestaurantProfile,AddRestaurant
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout
from django.views import View
from django.db.models import Q
from django.http import JsonResponse
from .models import RestaurantDish,RestaurantRegistration,OrderDish,DishCart
from django.contrib import messages



# Create your views here.
def restaurant(request):
    return render(request,"restaurant/restaurant.html")


# RESTAURANT SIGNUP
def restaurant_signup(request):
    if request.method == "POST":
        fm=RestaurantSignup(request.POST)
        if fm.is_valid():
            uname=fm.cleaned_data["username"]
            upass=fm.cleaned_data["password1"]
            fm.save()
            user=authenticate(username=uname,password=upass)
            if user is not None:
                login(request,user)
                print("restaurant owner signup successful")
                return HttpResponseRedirect("/restaurant/add_restaurant/")
    else:
        fm=RestaurantSignup()
    return render(request,"restaurant/restaurant_signup.html",{"forms":fm})


# Restaurant LOGIN 
def restaurant_login(request):
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
                    return render(request,"restaurant/restaurant_login.html")
        else:
            fm=AuthenticationForm()
    
    return render(request,"restaurant/restaurant_login.html",{"login_form":fm})



# Restaurant LOGOUT
def restaurant_logout(request):
    logout(request)
    return HttpResponseRedirect("/restaurant/restaurant_login/")



# RESTATURANT PROFILE
def restaurant_profile(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            fm=ShowRestaurantProfile(request.POST,instance=request.user)
            if fm.is_valid():
                fm.save()
        else:
            fm=ShowRestaurantProfile(instance=request.user)
        return render(request,"restaurant/restaurant_profile.html",{"name":request.user,"form":fm})
    else:
        return HttpResponseRedirect("/restaurant/restaurant_login/")
    



# CHANGE PASSWORD
def restaurant_change_pass(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            fm=PasswordChangeForm(user=request.user,data=request.POST)
            if fm.is_valid():
                fm.save()
                return HttpResponseRedirect("/restaurant/restaurant_profile/")
        else:
            fm=PasswordChangeForm(request)
        return render(request,"restaurant/change_password.html",{"change_pass_form":fm})
    else:
        return HttpResponseRedirect("/")

        

# class RestaurantDishView(View):
#     def get(request,self):
#         veg=RestaurantDish.objects.filter(Dish_type="V")
#         Availaible = RestaurantDish.objects.filter(Availaibility="Y")
#         return render(request,"core/home.html",{"veg":veg},{"Availaible":Availaible})


class ProductView(View):
    def get(self,request,pk):
        print("primary key:",pk)
        cart_product=DishCart.objects.filter(dish=pk)
        data=RestaurantDish.objects.get(pk=pk)
        return render(request,"restaurant/product_detail.html",{"product":data,"cart_product":cart_product})


def addrestaurant(request):
    if request.method== "POST":
        fm=AddRestaurant(request.POST , request.FILES)
        if fm.is_valid():
            restaurant=fm.save(commit=False)
            restaurant.user=request.user
            restaurant.save()
            print(restaurant)
            return redirect("show_restaurant_details" ,pk=restaurant.id)
    else:
        fm=AddRestaurant()
    return render(request,"restaurant/add_restaurant.html",{"form":fm})


# def show_restaurant_details(request,pk):
#     fm=RestaurantRegistration.objects.get(pk=pk)
#     print(pk)
#     print(fm)
#     return render(request,"restaurant/showrestaurantdetail.html",{"res_data":fm})

def show_restaurant_details(request,pk):
    restaurant=RestaurantRegistration.objects.get(pk=pk)
    if request.method == "POST":
        fm=AddRestaurant(request.POST,request.FILES,instance=restaurant)
        if fm.is_valid():
            fm.save()
            return HttpResponseRedirect("/")
    else:
        fm=AddRestaurant(instance=restaurant)
    return render(request,"restaurant/showrestaurantdetail.html",{"form":fm})
    

# def delete_restaurant_details(request,pk):
#     fm=RestaurantRegistration.objects.get(pk=pk)
#     fm.delete()
#     return render(request,"core/home.html")



def add_to_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart_data=DishCart.objects.filter(user=user)
        product_id=request.GET.get('prod_id')
        print(product_id)
        product=RestaurantDish.objects.get(pk=product_id)
        try:
            cart_item=DishCart.objects.get(dish=product)
            if cart_item:
                return redirect("/restaurant/show_cart/")
        except:
            print("It is a new item")
            
        restaurant=product.restaurant
        print(restaurant)
        if cart_data.exists():
            first_item=cart_data.first()
            if first_item.dish.restaurant != restaurant:
                messages.error(request,"You can order food from only one restaurant at a time.")
                return redirect("/menu/")

        cart_item=DishCart(user=user,dish=product)
        print("i am here ")
        cart_item.save()
                
    return  redirect("/restaurant/show_cart/")



def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart_data=DishCart.objects.filter(user=user)
        print(cart_data)
        amount=0
        total_price=0
        total_quantity =0
        for p in cart_data:
            total_quantity +=p.quantity
            amount=p.dish.Dis_price* p.quantity
            total_price += amount
            print(total_price)
        return render(request,"restaurant/show_cart.html",{"cart_data":cart_data,"total_price":total_price,"total_quantity":total_quantity})

def cart_plus_icon_click(request):
    if request.method == "GET":
        prod_id=request.GET.get("prod_id")
        print(prod_id)
        cart_data=DishCart.objects.get(Q(dish=prod_id))
        cart_data.quantity +=1
        cart_data.save()
        print(cart_data.quantity)
        amount=0
        total_price=0
        cart_items=DishCart.objects.all()
        for p in cart_items:
            amount=(p.quantity*p.dish.Dis_price)
            total_price += amount
        
        data={
            "amount":amount,
            "total_price":total_price,
            "quantity":cart_data.quantity,

        }

        return JsonResponse(data)

        




def cart_minus_icon_click(request):
    if request.method == "GET":
        prod_id=request.GET["prod_id"]
        cart_data=DishCart.objects.get(Q(dish=prod_id) & Q(user=request.user))
        cart_data.quantity -= 1
        cart_data.save()
        print(cart_data.quantity)
        amount=0
        total_amount=0
        cart_items=DishCart.objects.all()
        for p in cart_items:
            amount=(p.quantity*p.dish.Dis_price)
            total_amount +=amount    
            print("i have reached")    
        data={
            "total_amount":total_amount,
            "dish_quantity":cart_data.quantity
        }
    return JsonResponse(data)



def  cart_remove_button_click(request):
    if request.method == "GET":
        prod_id=request.GET["prod_id"]
        print(prod_id)
        cart_data=DishCart.objects.get(Q(dish=prod_id) & Q(user=request.user))
        cart_data.delete()
        amount=0
        total_amount=0
        cart_items=DishCart.objects.all()
        for p in cart_items:
            amount=(p.quantity*p.dish.Dis_price)
            total_amount +=amount    
            print("i have reached")    
        data={
            "total_amount":total_amount,
        }
    return JsonResponse(data)



def fav_dish(request,pk):
    dish=RestaurantDish.objects.get(pk=pk)
    fav_dish=request.session.get("fav_dish",{})
    if str(dish.id) in fav_dish:
        print("no dish added")
        alldish=request.session.get("fav_dish",{})
        # request.session.flush()
    else:
        fav_dish[str(dish.id)]={"Name":dish.Name,"Price":dish.Price,"Image":dish.Image.url}
        print("Dish added succesfully")
        request.session["fav_dish"]=fav_dish
        alldish=request.session.get("fav_dish",{})
        print(alldish.values())

    return render(request,"restaurant/fav_dish.html",{"alldish":alldish})

def delete_fav_dish(request,pk):
        fav_dish=request.session["fav_dish"]
        print("before",fav_dish)
        del fav_dish[str(pk)]
        request.session["fav_dish"]=fav_dish
        alldish= request.session.get("fav_dish")
        print("aftre",fav_dish)

        return render(request,"restaurant/fav_dish.html",{"alldish":alldish})