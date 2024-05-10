from django.contrib import auth
from django.db.models import Avg
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from basket.models import Basket
from goods.models import FavoriteProduct, Product, Review
from orders.models import OrderItem
from users.forms import ChangeProductForm, PaymentMethodForm, UserLoginForm, UserRegistrationForm, ProfileForm
from users.models import PaymentMethod

# Create your views here.
def LogIn(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            session_key = request.session.session_key

            if user:
                auth.login(request, user)

                if session_key:
                    Basket.objects.filter(session_key=session_key).update(user=user)

                redirect_page = request.POST.get('next', None)
                if redirect_page and redirect_page != reverse('user:logout'):
                    return HttpResponseRedirect(request.POST.get('next'))
                
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()

    context = {
        'title': 'Вход в учетную запись - Войдите в свой аккаунт для доступа к эксклюзивным предложениям',
        'form': form,
    }
    return render(request, 'users/log_in.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()

            session_key = request.session.session_key

            user = form.instance
            auth.login(request, user)

            if session_key:
                Basket.objects.filter(session_key=session_key).update(user=user)

            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'Регистрация на сайте ProSoftware - Присоединяйтесь к нашему интернет магазину прямо сейчас!',
        'form': form
    }
    return render(request, 'users/registration.html', context)


@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))


@login_required
def profile(request):

    user = request.user
    products = Product.objects.filter(manufacturer=user.id)
    average_rating = products.aggregate(avg_rating=Avg('review__rating'))['avg_rating']
    buy_history = OrderItem.objects.filter(order__user_id=user.id)
    fav_prod = FavoriteProduct.objects.filter(user=user)

    buy_history_slug = OrderItem.objects.filter(order__user_id=user.id).values_list('product__slug', flat=True)
    his_prod = Product.objects.filter(slug__in=buy_history_slug)
    reviews = []
    anti_reviews = []
    for product in his_prod:
        product_review = Review.objects.filter(product=product, user=user).order_by('-date_added').first()
        if product_review:
            reviews.append(product_review)
        else:
            anti_rating_review = Review(product=product, user=user, rating=5.0)
            anti_reviews.append(anti_rating_review)

    payment_methods = PaymentMethod.objects.filter(user=user)

    products_his = Product.objects.filter(manufacturer=user.id)[:4]
    buy_his = OrderItem.objects.filter(order__user_id=user.id)[:4]
    fav_his = FavoriteProduct.objects.filter(user=user)[:4]

    if average_rating is not None:
        average_rating_int = int(average_rating) or 0
        average_rating_float = average_rating - average_rating_int
        anti_average_rating = int(5 - average_rating)
    else:
        average_rating_int = None
        average_rating_float = None
        anti_average_rating = None

    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=request.user)

    context = {
        'title': 'Личный кабинет на сайте ProSoftware - Управляйте своими заказами и настройками в личном кабинете',
        'form': form,
        'reviews': reviews,
        'buy_his': buy_his,
        'fav_his': fav_his,
        'products': products,
        'fav_prod': fav_prod,
        'buy_history': buy_history,
        'products_his': products_his,
        'anti_reviews': anti_reviews,
        'average_rating': average_rating,
        'payment_methods': payment_methods,
        'average_rating_int': average_rating_int,
        'anti_average_rating': anti_average_rating,
        'average_rating_float': average_rating_float,
    }

    return render(request, 'users/user_page.html', context)


@login_required
def save_payment_method(request):
    user = request.user

    if request.method == 'POST':
        form = PaymentMethodForm(data=request.POST)
        if form.is_valid():
            payment_method = form.save(commit=False)
            payment_method.user = user
            payment_method.save()
            return redirect('users:profile')
    else:
        form = PaymentMethodForm()

    context = {
        'form': form,
    }

    return render(request, 'users/save_payment_method.html', context)


@login_required
def save_payment_method_id(request):
    user = request.user

    if request.method == 'POST':
        payment_method_id = request.POST.get('payment_method')
        try:
            payment_method = PaymentMethod.objects.get(pk=payment_method_id)
            user.payment_method = payment_method
            user.save()
            return JsonResponse({'success': True})
        except PaymentMethod.DoesNotExist:
            return JsonResponse({'error': 'Способ оплаты не найден'}, status=404)

    return JsonResponse({'error': 'Недопустимый запрос'}, status=400)


@login_required
def add_favorite_product(request):
    product_slug = request.POST.get("product_slug")
    product = Product.objects.get(slug=product_slug)
    if request.user.is_authenticated:
        FavoriteProduct.objects.create(user=request.user, product=product)
        redirect_url = reverse('catalog:product', kwargs={'product_slug': product_slug})
        return redirect(redirect_url)
    

@login_required
def remove_favorite_product(request):
    if request.method == 'POST':
        product_slug = request.POST.get("product_slug")
        product = Product.objects.get(slug=product_slug)
        favorite_product = FavoriteProduct.objects.filter(user=request.user, product=product)
        if favorite_product.exists():
            favorite_product.delete()
            redirect_url = reverse('catalog:product', kwargs={'product_slug': product_slug})
            return redirect(redirect_url)
        
@login_required
def Change_User_product(request):
    if request.method == 'POST':
        if 'delete_product' in request.POST:
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, pk=product_id)
            product.delete()
            return redirect('users:profile')
        else:
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, pk=product_id)
            form = ChangeProductForm(request.POST, files=request.FILES, instance=product)
            if form.is_valid():
                product = form.save(commit=False)
                product.manufacturer = request.user
                discount_percentage = form.cleaned_data['discount_percentage']
                product.discount_percentage = discount_percentage
                product.save()
                return redirect('users:profile')