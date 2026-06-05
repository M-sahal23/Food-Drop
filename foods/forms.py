from django import forms
from foods.models import FoodItems, CustomizedCart


class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItems
        fields = ['name', 'price', 'rating', 'desc', 'category', 'food_img']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'food_img': forms.FileInput(attrs={'class': 'form-control'}),
        }


class CustomizationForm(forms.ModelForm):
    """Form for customizing food items"""
    class Meta:
        model = CustomizedCart
        fields = ['quantity', 'size', 'base', 'sauce', 'toppings']
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1'
            }),
            'size': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'base': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'sauce': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'toppings': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }


from django import forms
from foods.models import Review

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.HiddenInput()      # we handle stars in JS
    )

    class Meta:
        model   = Review
        fields  = ['reviewer', 'rating', 'comment']
        widgets = {
            'reviewer': forms.TextInput(attrs={
                'class':       'form-control',
                'placeholder': 'Your name',
            }),
            'comment': forms.Textarea(attrs={
                'class':       'form-control',
                'placeholder': 'Write your review...',
                'rows':        3,
            }),
        }
        labels = {
            'reviewer': 'Your Name',
            'comment':  'Your Review',
        }