import re
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from basket.models import Basket
from basket.utils import get_user_basket
from goods.models import Product

# Create your views here.
def basket_add(request):
    
    product_id = request.POST.get("product_id")
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user, product=product)

        if basket.exists():
            basket = basket.first()
            if basket:
                basket.quantity += 1
                basket.save()
        else:
            Basket.objects.create(user=request.user, product=product, quantity=1)

    user_basket = get_user_basket(request)
    basket_items_html = render_to_string(
        "basket/shopping_basket_page.html", {"baskets": user_basket}, request=request
    )

    response_data = {
        "basket_items_html": basket_items_html,
    }

    return JsonResponse(response_data)

def basket_change(request, product_slug):
    pass

def basket_remove(request, basket_id):
    
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    
    return redirect(request.META['HTTP_REFERER'])

def shopping_basket(request):
    return render(request, 'basket/shopping_basket_page.html')