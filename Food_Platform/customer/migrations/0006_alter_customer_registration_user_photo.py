# Generated by Django 4.2.13 on 2024-06-08 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_alter_customer_registration_user_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer_registration',
            name='User_Photo',
            field=models.ImageField(blank=True, default='media/defaultuser.jpg', null=True, upload_to='User_Images/'),
        ),
    ]
