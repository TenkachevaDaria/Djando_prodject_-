from django.urls import path

from main import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('user/', views.user, name='user'),
    path('add_product/', views.addProduct, name='addProduct'),
    path("login/", views.LogIn, name="LogIn"),
    path("registration/", views.registration, name="registration"),
    path("shopping_basket/", views.shopping_basket, name="shopping_basket"),
]
