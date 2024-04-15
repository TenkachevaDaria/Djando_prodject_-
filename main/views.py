from django.http import HttpResponse
from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
    questions = Questions.objects.all()
    return render(request, 'main/index.html', {'questions': questions})

def addProduct(request):
    return render(request, 'main/add_product_page.html')


def shopping_basket(request):
    return render(request, 'main/shopping_basket_page.html')