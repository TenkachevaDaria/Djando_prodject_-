from django.shortcuts import render
from django.template import context

# Create your views here.
def catalog(request):
    context: dict[str, str] = {
        'title': 'Home - Каталог',
        'goods':  [
            {
                'name': 'название',
                'price': '250',
                'sale': 'no',
            },

            {
                'name': 'название',
                'price': '250',
                'sale': 'no',
            },
            {
                'name': 'название',
                'price': '250',
                'sale': 'no',
            },
            
            
        ]
    }
    return render(request, 'goods/products.html', context)

def product(request):
    return render(request, 'goods/product_page.html')