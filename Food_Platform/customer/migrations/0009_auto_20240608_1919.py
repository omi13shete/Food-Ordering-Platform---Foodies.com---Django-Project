# <app_name>/migrations/000X_auto_set_default_user_photos.py

from django.db import migrations, models

def set_default_user_photos(apps, schema_editor):
    Customer_Registration = apps.get_model('customer', 'Customer_Registration')
    for customer in Customer_Registration.objects.all():
        if not customer.User_Photo:
            customer.User_Photo = 'defaultuser.jpg'
            customer.save()

class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_alter_customer_registration_user_photo'),
    ]

    operations = [
        migrations.RunPython(set_default_user_photos),
    ]
