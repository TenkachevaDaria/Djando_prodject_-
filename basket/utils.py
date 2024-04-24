from basket.models import Basket
from users.models import PaymentMethod


def get_user_basket(request):
    if request.user.is_authenticated:
        return Basket.objects.filter(user=request.user)
    
    if not request.session.session_key:
        request.session.create()
    return Basket.objects.filter(session_key=request.session.session_key)


def get_user_payment(request):
    if request.user.is_authenticated:
        return PaymentMethod.objects.filter(user=request.user)