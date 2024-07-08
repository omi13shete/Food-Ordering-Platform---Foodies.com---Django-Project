from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer_Profile(models.Model):
    User=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    User_Photo=models.ImageField(upload_to="User_Images/",default="defaultuser.jpg")
    Fullname = models.CharField(max_length=50)
    contact_no=models.IntegerField(max_length=10,default=None,null=True,blank=True)
    Email = models.CharField(max_length=70)
    Address = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)
    Repeat_password = models.CharField(max_length=50)
    # profile_picture=models.ImageField()

    def __str__(self):
        return str(self.Fullname)



