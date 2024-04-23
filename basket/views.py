import re
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from basket.models import Basket
from basket.utils import get_user_basket
from goods.models import Product
from users.models import PaymentMethod

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

    else:
        basket = Basket.objects.filter(session_key=request.session.session_key, product=product)

        if basket.exists():
            basket = basket.first()
            if basket:
                basket.quantity += 1
                basket.save()
        else:
            Basket.objects.create(session_key=request.session.session_key, product=product, quantity=1)


    user_basket = get_user_basket(request)
    basket_items_html = render_to_string(
        "basket/include/basket.html", {"baskets": user_basket}, request=request
    )

    response_data = {
        "basket_items_html": basket_items_html,
    }

    return JsonResponse(response_data)


def basket_change(request):
    basket_id = request.POST.get("basket_id")
    quantity = request.POST.get("quantity")

    basket = Basket.objects.get(id=basket_id)

    basket.quantity = quantity
    basket.save()
    updated_quantity = basket.quantity

    basket = get_user_basket(request)
    basket_items_html = render_to_string(
        "basket/include/basket.html", {"baskets": basket}, request=request
    )

    response_data = {
        "basket_items_html": basket_items_html,
        "quantity": updated_quantity,
    }

    return JsonResponse(response_data)


def basket_remove(request):
    
    basket_id = request.POST.get("basket_id")
    basket = Basket.objects.get(id=basket_id)
    quantity = basket.quantity
    basket.delete()

    user_basket = get_user_basket(request)
    basket_items_html = render_to_string(
        "basket/include/basket.html", {"baskets": user_basket}, request=request
    )

    response_data = {
        "basket_items_html": basket_items_html,
        "quantity": quantity,
    }

    return JsonResponse(response_data)

@login_required
def shopping_basket(request):
    user = request.user
    payment_methods = PaymentMethod.objects.filter(user_id=user.id)
    context = {
        'payment_methods': payment_methods,
    }
    return render(request, 'basket/shopping_basket_page.html', context)