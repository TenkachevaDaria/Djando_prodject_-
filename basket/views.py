import re
from django.shortcuts import redirect, render

from basket.models import Basket
from goods.models import Product

# Create your views here.
def basket_add(request, product_slug):
    
    product = Product.objects.get(slug=product_slug)

    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user, product=product)

        if basket.exists():
            basket = basket.first()
            if basket:
                basket.quantity += 1
                basket.save()
        else:
            Basket.objects.create(user=request.user, product=product, quantity=1)

    return redirect(request.META['HTTP_REFERER'])

def basket_change(request, product_slug):
    pass

def basket_remove(request, basket_id):
    
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    
    return redirect(request.META['HTTP_REFERER'])

def shopping_basket(request):
    return render(request, 'basket/shopping_basket_page.html')