from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = User.ROLE_CHOICES  # fetch from User model

    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)
    
    class Meta:
        model = User
        fields = ("username", "email", "role")

class CustomUserChangeForm(forms.ModelForm):
    ROLE_CHOICES = User.ROLE_CHOICES  # fetch from User model

    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)
    class Meta:
        model = User
        fields = ("username", "email", "role")