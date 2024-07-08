from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.

class RestaurantRegistration(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=50, default='Indian Food Restaurant')
    image = models.ImageField(upload_to='restaurants/', default="defaultuser.jpg", null=True, blank=True)
    location = models.CharField(max_length=50, default="Mumbai")
    cost_for_two = models.DecimalField(max_digits=8, decimal_places=2, default=800.00)

    def __str__(self):
        return f"{self.restaurant_name}"

Dish_Type=(
    ("V","veg"),
    ("NV","Nonveg"),
    ("S","Snacks"),
    ("BF","Breakfast")
)

Availability=(("YES","yes"),("NO","no"))

class RestaurantDish(models.Model):
    restaurant =models.ForeignKey(RestaurantRegistration,on_delete=models.CASCADE, related_name="dishes" ,null=True, blank= True)
    Type=models.CharField(max_length=50,default="Dish")
    Description =models.CharField(max_length=5000, default='A dish is a specific preparation of food that is created by combining various ingredients and cooking them according to a particular recipe or method. Dishes can range from simple to complex and can be served as part of a meal or as a standalone item. They can be hot or cold, sweet or savory, and can come from any cuisine around the world.')
    Name=models.CharField(max_length=70)    
    Image=models.ImageField(upload_to="Dish_Images/")
    DishType=models.CharField(choices=Dish_Type,max_length=30)
    Availability=models.CharField(choices=Availability,max_length=50)
    Price=models.IntegerField(max_length=5)
    Dis_price=models.IntegerField(max_length=5)

    def __str__(self):
        return str(self.Name)



class OrderDish(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    dish = models.ForeignKey(RestaurantDish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField( default=1)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey(RestaurantRegistration, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    dishes = models.ManyToManyField(RestaurantDish, through=OrderDish)

    def get_dishes(self):
        return ", ".join([str(dish) for dish in self.dishes.all()])

    get_dishes.short_description = 'Dishes'


class DishCart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    dish=models.ForeignKey(RestaurantDish,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)




class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    restaurant = models.ForeignKey(RestaurantRegistration, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


