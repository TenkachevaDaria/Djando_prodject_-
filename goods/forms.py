from django import forms

from goods.models import Review

# class CreateOrderForm(forms.Form):
class AddReview(forms.ModelForm):

    class Meta:
        model = Review
        fields = {
            'rating',
            'comment',
        }

    comment = forms.CharField()
    rating = forms.ChoiceField()