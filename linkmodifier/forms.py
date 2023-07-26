from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from .models import Link

class CreateNewUser(UserCreationForm):
    model = User
    fields = ['username', 'password1', 'password2']

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['title', 'url_link']

class QRForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['title']

    def save(self, commit=True):
        pass





