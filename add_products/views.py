from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from add_products.forms import AddProductForm
import logging
from goods.models import Subscriptions
from goods.views import Categories


logger = logging.getLogger(__name__)

# Create your views here.
@login_required
def AddProduct(request):

    categories = Categories.objects.exclude(name='Все')
    subscriptions = Subscriptions.objects.all()

    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.manufacturer = request.user
            product.save()
            return redirect('users:profile')
    else:
        form = AddProductForm()

    context = {
        'form': form,
        'categories': categories,
        'subscriptions': subscriptions
    }

    return render(request, 'add_product/add_product.html', context)