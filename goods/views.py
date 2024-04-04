from unicodedata import category
from django.db.models import Avg
from django.shortcuts import render
from django.template import context
from .models import Categories, Product, Review

# Create your views here.
def catalog(request):
    products = Product.objects.all()
    categories = Categories.objects.all()

    context = {
        'categories': categories,
        'products': products
    }
    return render(request, 'goods/products.html', context)

def product(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    reviews = Review.objects.filter(product=product)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    review_ratings = [5 - review.rating for review in reviews]

    context = {
        'product': product,
        'reviews': reviews,
        'average_rating': average_rating,
        'average_rating_int': int(average_rating),
        'average_rating_float': average_rating - int(average_rating),
        'anti_average_rating': int(5 - average_rating),
        'review_ratingds': review_ratings
    }
    return render(request, 'goods/product_page.html', context)