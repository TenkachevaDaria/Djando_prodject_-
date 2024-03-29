from django.http import HttpResponse
from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
    questions = Questions.objects.all()
    return render(request, 'main/index.html', {'questions': questions})

def user(request):
    return render(request, 'main/user_page.html')

def addProduct(request):
    return render(request, 'main/add_product_page.html')

def LogIn(request):
    return render(request, 'main/log_in.html')

def registration(request):
    return render(request, 'main/registration.html')

def shopping_basket(request):
    return render(request, 'main/shopping_basket_page.html')