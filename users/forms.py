from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from goods.models import FavoriteProduct
from users.models import PaymentMethod, User

class UserLoginForm(AuthenticationForm):

    username = forms.CharField()
    password = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegistrationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = {
            'username',
            'email',
            'password1',
            'password2',
        }

    username = forms.CharField()
    email = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()


class ProfileForm(UserChangeForm):
    
    class Meta:
        model = User
        fields = {
            'image',
            'first_name',
            'last_name',
            'middle_name',
            'email',
            'phone',
        }

    image = forms.ImageField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    middle_name = forms.CharField(required=False)
    email = forms.CharField(required=False)
    phone = forms.CharField(required=False)


class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ('card_num', 'date', 'CVV', 'bank')
        
    card_num = forms.CharField()
    date = forms.CharField()
    CVV = forms.CharField()
    bank = forms.CharField()