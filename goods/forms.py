from django import forms

from goods.models import Review

# class CreateOrderForm(forms.Form):
class AddReview(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ['date_added']

    rating = forms.ChoiceField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], label='Рейтинг')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
