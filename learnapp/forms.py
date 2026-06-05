from django import forms
from django.contrib.auth.models import User
from learnapp.models import UserDetails
from django_recaptcha.fields import ReCaptchaField


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        # fields = "__all__"
        fields = ['username', 'email', 'password']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['phone', 'address', 'street', 'city', 'zipcode', 'profile_pic', 'user_type'] # We cannot use __all__ because it gives error for one to one field so we use in list form
    captcha = ReCaptchaField()

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['phone', 'address', 'street', 'city', 'zipcode', 'profile_pic']