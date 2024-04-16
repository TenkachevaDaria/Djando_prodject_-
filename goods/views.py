from django.core.paginator import Paginator
from django.db.models import Avg, Max, Min
from django.shortcuts import render

from goods.utils import q_search
from goods.models import Categories, Product, Specification, Subscriptions, Review

# Create your views here.
from django.db.models import Q

def catalog(request):
    
    page = request.GET.get('page', 1)
    order_by = request.GET.get('order_by', None)
    subscription_filter = request.GET.get('subscription', None)
    in_stock_filter = request.GET.get('in_stock', None)
    category_filter = request.GET.get('category', None)
    price_filter_from = request.GET.get('sort_price_from', None)
    price_filter_to = request.GET.get('sort_price_to', None)
    query = request.GET.get('q', None)
    
    products = Product.objects.all()
    categories = Categories.objects.all()
    subscriptions = Subscriptions.objects.all()

    max_price = products.aggregate(max_price=Max('price'))['max_price']
    min_price = products.aggregate(min_price=Min('price'))['min_price']

    if query:
        products = q_search(query)


    if order_by == '-avg_rating':
        products = products.annotate(avg_rating=Avg('review__rating')).order_by('-avg_rating')
    elif order_by and order_by != "default":
        products = products.order_by(order_by)


    if price_filter_from:
        products = products.filter(price__gte=float(price_filter_from))
    if price_filter_to:
        products = products.filter(price__lte=float(price_filter_to))

    if subscription_filter:
        products = products.filter(subscription=subscription_filter)

    if in_stock_filter == 'true':
        products = products.filter(in_stock=True)

    if category_filter:
        products = products.filter(category=category_filter)

    paginator = Paginator(products, 24)
    current_page = paginator.page(page)

    context = {
        'categories': categories,
        'subscriptions': subscriptions,
        'products': current_page,
        'max_price': max_price,
        'min_price': min_price
    }
    return render(request, 'goods/products.html', context)


def product(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    reviews = Review.objects.filter(product=product)
    specifications = Specification.objects.filter(product=product)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    review_ratings = [5 - review.rating for review in reviews]

    if average_rating is not None:
        average_rating_int = int(average_rating) or 0
        average_rating_float = average_rating - average_rating_int
        anti_average_rating = int(5 - average_rating)
    else:
        average_rating_int = None
        average_rating_float = None
        anti_average_rating = None

    context = {
        'product': product,
        'reviews': reviews,
        'average_rating': average_rating,
        'average_rating_int': average_rating_int,
        'average_rating_float': average_rating_float,
        'anti_average_rating': anti_average_rating,
        'review_ratings': review_ratings,
        'specifications': specifications
    }

    return render(request, 'goods/product_page.html', context)