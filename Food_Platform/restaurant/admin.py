from django.contrib import admin
from .models import RestaurantRegistration,RestaurantDish,Order,OrderDish,Review,DishCart
# Register your models here.


@admin.register(RestaurantRegistration)
class Restaurant_admin(admin.ModelAdmin):
    list_display=["restaurant_name","image","location","cost_for_two"]
    

@admin.register(RestaurantDish)
class  RestaurantDishAdmin(admin.ModelAdmin):
    list_display=["restaurant","Name","Image","Description","DishType","Price","Dis_price","Availability"]


@admin.register(Order)
class  OrderAdmin(admin.ModelAdmin):
    list_display=["user","restaurant","created_at","total_price","get_dishes"]

@admin.register(Review)
class  ReviewAdmin(admin.ModelAdmin):
    list_display=["user","restaurant","rating","comment","created_at"]

@admin.register(OrderDish)
class  OrderDishAdmin(admin.ModelAdmin):
    list_display=["order","dish","quantity"]

@admin.register(DishCart)
class  DishCartAdmin(admin.ModelAdmin):
    list_display=["user","dish","quantity"]

