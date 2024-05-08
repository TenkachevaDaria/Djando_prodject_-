from django.core.paginator import Paginator
from django.db.models import Avg, Max, Min
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from goods.forms import AddReview
from goods.utils import q_search
from goods.models import Categories, FavoriteProduct, Product, Subscriptions, Review
from users.models import User

# Create your views here.
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
        products = products.order_by('-average_rating')
    elif order_by and order_by != "default":
        products = products.order_by(order_by)


    if price_filter_from:
        products = products.filter(price__gte=float(price_filter_from))
    if price_filter_to:
        products = products.filter(price__lte=float(price_filter_to))

    if subscription_filter:
        products = products.filter(subscription=subscription_filter)

    if in_stock_filter and in_stock_filter != "default":
        products = products.filter(in_stock=in_stock_filter)

    if category_filter:
        products = products.filter(category=category_filter)

    paginator = Paginator(products, 24)
    current_page = paginator.page(page)

    context = {
        'title': 'Каталог ПО на сайте  ProSoftware - Исследуйте наш широкий ассортимент программных продуктов',
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
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    if request.user.is_authenticated:
        fav_prod = FavoriteProduct.objects.filter(product=product.id, user=request.user).exists()
    order_by = request.GET.get('order_by', None)

    if order_by and order_by != "default":
        reviews = reviews.order_by(order_by)

    if average_rating is not None:
        average_rating_int = int(average_rating) or 0
        average_rating_float = average_rating - average_rating_int
        anti_average_rating = int(5 - average_rating)
    else:
        average_rating_int = None
        average_rating_float = None
        anti_average_rating = None

    if request.user.is_authenticated:
        context = {
            'title': '- Узнайте больше о продукте и его возможностях',
            'product': product,
            'reviews': reviews,
            'fav_prod': fav_prod,
            'average_rating': average_rating,
            'average_rating_int': average_rating_int,
            'average_rating_float': average_rating_float,
            'anti_average_rating': anti_average_rating,
            'total_reviews_count': reviews.count()
        }
    else:
        context = {
            'title': '- Узнайте больше о продукте и его возможностях',
            'product': product,
            'reviews': reviews,
            'average_rating': average_rating,
            'average_rating_int': average_rating_int,
            'average_rating_float': average_rating_float,
            'anti_average_rating': anti_average_rating,
            'total_reviews_count': reviews.count()
        }

    return render(request, 'goods/product_page.html', context)


@login_required
def addReviews(request):
    if request.method == 'POST':
        form = AddReview(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.save()
            product_slug = form.cleaned_data['product'].slug
            redirect_url = reverse('catalog:product', kwargs={'product_slug': product_slug})
            return redirect(redirect_url)
    else:
        form = AddReview()
    return render(request, 'goods/product_page.html', {'form': form})