# Generated by Django 4.2.13 on 2024-06-24 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0006_dishcart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantdish',
            name='Availability',
            field=models.CharField(choices=[('YES', 'yes'), ('NO', 'no')], max_length=50),
        ),
    ]