from django.contrib import auth
from django.db.models import Avg
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from basket.models import Basket
from goods.models import Product, Review
from orders.models import Order, OrderItem
from users.forms import PaymentMethodForm, UserLoginForm, UserRegistrationForm, ProfileForm
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
    buy_history = OrderItem.objects.filter(order__user_id=user.id)
    average_rating = products.aggregate(avg_rating=Avg('review__rating'))['avg_rating']
    payment_methods = PaymentMethod.objects.filter(user=user)

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
        'form': form,
        'products': products,
        'average_rating': average_rating,
        'average_rating_int': average_rating_int,
        'average_rating_float': average_rating_float,
        'anti_average_rating': anti_average_rating,
        'payment_methods': payment_methods,
        'buy_history': buy_history,
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