from django import forms
from django.contrib.auth.models import User

# Create your models here.

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ("username", "password")