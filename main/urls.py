from django.urls import path

from main import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('add_product/', views.addProduct, name='addProduct'),
    path("shopping_basket/", views.shopping_basket, name="shopping_basket"),
]
