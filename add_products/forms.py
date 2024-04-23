from unicodedata import category
from django.forms import widgets
from goods.models import Categories, Product, Subscriptions
from django import forms




class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "name",
            "price",
            "category",
            "delivery_type",
            "media_type",
            "purpose",
            "subscription",
            "bitness",
            "description",
            "image",
        )

    # Определите поля формы
    name = forms.CharField(label="Название продукта")
    price = forms.DecimalField(label="Стоимость")
    category = forms.ModelChoiceField(queryset=Categories.objects.all(), label="Под какую систему предназначен ваш продукт?")
    delivery_type = forms.CharField(label="Тип поставки")
    media_type = forms.CharField(label="Тип носителя")
    purpose = forms.CharField(label="Назначение продукта")
    subscription = forms.ModelChoiceField(queryset=Subscriptions.objects.all(), label="Срок лицензии")
    bitness = forms.ChoiceField(choices=[('x32', 'x32'), ('x64', 'x64'), ('x86', 'x86')], label="Разрядность")
    description = forms.CharField(widget=forms.Textarea, label="Описание")
    image = forms.ImageField(label="Изображение продукта")