from unicodedata import category
from django.shortcuts import render
from django.template import context
from .models import Categories, Product

# Create your views here.
def catalog(request):
    products = Product.objects.all()
    categories = Categories.objects.all()
    return render(request, 'goods/products.html', {'products': products, 'categories': categories})

def product(request):
    return render(request, 'goods/product_page.html')