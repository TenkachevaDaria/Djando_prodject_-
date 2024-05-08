from django.http import HttpResponse
from django.shortcuts import render

from goods.models import Product
from .models import *

# Create your views here.
def index(request):
    questions = Questions.objects.all()
    products = Product.objects.all()[:3]

    context = {
        'title': 'Интернет-магазин ProSoftware - Добро пожаловать в мир высококачественного программного обеспечения',
        'questions': questions,
        'products': products
    }

    return render(request, 'main/index.html', context)