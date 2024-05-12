from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):  # Model forms allow us to make changes to model databases. in our case it is User db
    # username = forms.InlineForeignKeyField()
    class Meta:
        model = User
        fields = ["username"]


class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = Profile
        fields = ["email", "about", "image"]
