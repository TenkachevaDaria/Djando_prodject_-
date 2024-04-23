from django import forms

# class CreateOrderForm(forms.Form):
class CreateOrderForm(forms.Form):

    payment_method = forms.CharField(widget=forms.HiddenInput())
    email = forms.EmailField()