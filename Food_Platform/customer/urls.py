from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("customer-signup",views.customer_signup,name="customer-signup"),
    path('customer_login/', views.customer_login, name="customer_login"),
    path('customer_logout/', views.customer_logout, name="customer_logout"),
    path('customer_profile/', views.customer_profile, name="customer_profile"),
    path('customer_change_pass/', views.customer_change_pass, name="customer_change_pass"),
    path('add_customer_details/', views.add_customer_details, name="add_customer_details"),
    path('show_customer_details/<int:pk>/', views.show_customer_details, name="show_customer_details"),
    path('delete_customer_details/<int:pk>/', views.delete_customer_details, name="delete_customer_details"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)