from django.shortcuts import render
from restaurant.models import RestaurantDish,RestaurantRegistration,DishCart
# view function for the homepage
def home(request):
    if request.user.is_authenticated:
        cart_data=DishCart.objects.filter(user=request.user)
        total_quantity =0
        for p in cart_data:
            total_quantity +=p.quantity
    else:
        total_quantity=0
    veg=RestaurantDish.objects.filter(DishType="V")
    Nonveg=RestaurantDish.objects.filter(DishType="NV")
    restaurant=RestaurantRegistration.objects.all
    return render(request,"core/home.html",{"Veg_Dishes":veg,"Nonveg_Dishes":Nonveg,"restaurants":restaurant,"total_quantity":total_quantity})


def about(request):
    cart_data=DishCart.objects.filter(user=request.user)
    total_quantity =0
    for p in cart_data:
        total_quantity +=p.quantity
    print(request)
    return render(request,"core/about.html",{"total_quantity":total_quantity})

def contact(request):
    cart_data=DishCart.objects.filter(user=request.user)
    total_quantity =0
    for p in cart_data:
        total_quantity +=p.quantity
    print(request)
    return render(request,"core/contact.html",{"total_quantity":total_quantity})


# def menu(request,data=None):
#     if data==None:
#         dishes_data=RestaurantDish.objects.filter(Type="Dish")
#         print(dishes_data)
#     elif data=="V" or data=="NV":
#         print(data)
#         dishes_data=RestaurantDish.objects.filter(DishType=data)
#         print(dishes_data)
#     return render(request,"core/menu.html",{"all_dishes":dishes_data})

def menu(request,price=None,data=None):
    print(data)
    print(price)
    cart_data=DishCart.objects.filter(user=request.user)
    total_quantity =0
    for p in cart_data:
        total_quantity +=p.quantity
    print(request)
    if data==None:
        dishes_data=RestaurantDish.objects.filter(Type="Dish")
        print(dishes_data)
    elif data=="V":
        print(data)
        dishes_data=RestaurantDish.objects.filter(DishType=data)
        if price=="less than 399":
            dishes_data=RestaurantDish.objects.filter(DishType=data).filter(Dis_price__lt=399)
            print(dishes_data)
        elif price=="more than 399":
            dishes_data=RestaurantDish.objects.filter(DishType=data).filter(Dis_price__gt=399)
    elif data=="NV":
        print(data)
        dishes_data=RestaurantDish.objects.filter(DishType=data)
        if price=="less than 399":
            dishes_data=RestaurantDish.objects.filter(DishType=data).filter(Dis_price__lt=399)
            print(dishes_data)
        elif price=="More than 399":
            dishes_data=RestaurantDish.objects.filter(DishType=data).filter(Dis_price__gt=399)
    return render(request,"core/menu.html",{"all_dishes":dishes_data,"total_quantity":total_quantity,"cart_data":cart_data})

def login(request):
    print(request)
    return render(request,"core/login.html")

def signup(request):
    print(request)
    return render(request,"core/signup.html")