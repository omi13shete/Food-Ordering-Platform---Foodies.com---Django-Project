from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('res_page/', views.restaurant, name="restaurant"),
    path('restaurant-signup/', views.restaurant_signup, name="restaurant-signup"),
    path('restaurant_login/', views.restaurant_login, name="restaurant_login"),
    path('restaurant_logout/', views.restaurant_logout, name="restaurant_logout"),
    path('restaurant_profile/', views.restaurant_profile, name="restaurant_profile"),
    path('restaurant_change_pass/', views.restaurant_change_pass, name="restaurant_change_pass"),
    path('product_detail/<int:pk>', views.ProductView.as_view(), name="product_detail"),
    path('add_restaurant/', views.addrestaurant, name="add_restaurant"),
    path('show_restaurant_details/<int:pk>/', views.show_restaurant_details, name="show_restaurant_details"),
    # path('delete_restaurant_details/<int:pk>/', views.delete_restaurant_details, name="delete_restaurant_details"),
    path('add_to_cart/', views.add_to_cart, name="add_to_cart"),
    path('show_cart/', views.show_cart, name="show_cart"),
    path('cart_plus_icon_click/', views.cart_plus_icon_click, name="cart_plus_icon_click"),
    path('cart_minus_icon_click/', views.cart_minus_icon_click, name="cart_minus_icon_click"),
    path('cart_remove_button_click/', views.cart_remove_button_click, name="cart_remove_button_click"),
    path('fav_dish/<int:pk>', views.fav_dish, name="fav_dish"),
    path('delete_fav_dish/<int:pk>', views.delete_fav_dish, name="delete_fav_dish"),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)