# Generated by Django 4.2.13 on 2024-06-08 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0010_alter_customer_registration_user_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer_registration',
            name='User_Photo',
            field=models.ImageField(default='defaultuser.jpg', upload_to='User_Images/'),
        ),
    ]