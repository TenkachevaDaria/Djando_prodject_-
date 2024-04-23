from django.urls import path
from add_products import views

app_name = 'add_products'

urlpatterns = [
    path("add-product/", views.AddProduct, name="add_products"),
]
