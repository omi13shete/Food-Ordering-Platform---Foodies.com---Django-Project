from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("customer_checkout",views.customer_checkout,name="customer_checkout"),
    path("order_created",views.order_created,name="order_created"),
    path('demo/checkout/api/paypal/order/create/', views.create_order, name='create_order'),
    path('demo/checkout/api/paypal/order/<str:order_id>/capture/', views.capture_order, name='capture_order'),
    # path('razorpay_checkout', views.razorpay_checkout, name='razorpay_checkout'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)