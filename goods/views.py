from unicodedata import category
from django.shortcuts import render
from django.template import context
from .models import Categories, Product

# Create your views here.
def catalog(request):
    products = Product.objects.all()
    categories = Categories.objects.all()

    context = {
        'categories': categories,
        'products': products
    }
    return render(request, 'goods/products.html', context)

def product(request, product_slug):
    product = Product.objects.get(slug=product_slug)

    return render(request, 'goods/product_page.html', {'product': product})