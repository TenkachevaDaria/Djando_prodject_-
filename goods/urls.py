from django.urls import path
from goods import views

app_name = 'goods'

urlpatterns = [
    path('search/', views.catalog, name='search'),
    path('', views.catalog, name='index'),
    path('product/<slug:product_slug>/', views.product, name='product'),
    path('addReviews/', views.addReviews, name='addReviews'),
]
