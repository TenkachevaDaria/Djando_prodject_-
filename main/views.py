from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def user(request):
    return render(request, 'main/user_page.html')

def addProduct(request):
    return render(request, 'main/add_product_page.html')

def LogIn(request):
    return render(request, 'main/log_in.html')

def products(request):
    return render(request, 'main/products.html')

def registration(request):
    return render(request, 'main/registration.html')

def shopping_basket(request):
    return render(request, 'main/shopping_basket_page.html')