# Generated by Django 4.2.13 on 2024-06-11 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_order_restaurantdish_restaurant_review_orderdish_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantregistration',
            name='cost_for_two',
            field=models.DecimalField(decimal_places=2, default=800.0, max_digits=8),
        ),
    ]
