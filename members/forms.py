from django import forms
from django.contrib.auth.forms import UserCreationForm
from . models import CustomUser



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required')

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password1', 'password2']
        exclude = ['is_admin', 'is_active', 'is_superuser']