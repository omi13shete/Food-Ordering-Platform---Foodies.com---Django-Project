from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('menu/', views.menu, name="menu"),
    path('menu/<str:price>/<str:data>/', views.menu, name="specificmenu"),
    path('menu/<str:data>/', views.menu, name="menucategory"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup")

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)