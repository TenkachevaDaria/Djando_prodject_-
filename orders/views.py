from xml.dom import ValidationErr
from django.db import transaction
from django.db.models import F
from django.shortcuts import redirect, render

from basket.models import Basket
from goods.models import Product
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem

# Create your views here.
def create_order(request):
    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    basket_items = Basket.objects.filter(user=user)

                    if basket_items.exists():
                        order = Order.objects.create(
                            user=user,
                            email=form.cleaned_data['email'],
                            payment_method=form.cleaned_data['payment_method'],
                        )

                        for basket_item in basket_items:
                            product = basket_item.product
                            name = basket_item.product.name
                            if basket_item.product.discount_percentage:
                                price = basket_item.product.discount_price()
                            else:
                                price = basket_item.product.price
                            quantity = basket_item.quantity

                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity,
                            )
                            
                            Product.objects.filter(id=product.id).update(popularity=F('popularity') + quantity)
                        basket_items.delete()
                        return redirect('users:profile')

            except Exception as e:
                return redirect('basket:shopping_basket')

    form = CreateOrderForm()
    context = {
        'title': 'Оформить заказ - Интернет-магазин ПО ProSoftware',
        'form': form,
    }

    return render(request, 'orders/create_order.html', context=context)

