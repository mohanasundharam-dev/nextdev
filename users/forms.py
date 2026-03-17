from django.forms import ModelForm
from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields=['first_name','email','username','password1','password2']
        labels={
            'first_name':'Name',
        }

class ProfileForm(ModelForm):

    username = forms.CharField(max_length=150)

    class Meta:
        model = Profile
        exclude = ['user','id','created']

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username__iexact=username).exclude(id=self.instance.user.id).exists():
            raise forms.ValidationError("Username already taken")

        return username

class UsernameOrEmailPasswordResetForm(PasswordResetForm):
    email = forms.CharField(
        max_length=254,
        label="Username or Email"
    )

    def clean_email(self):
        value = self.cleaned_data["email"]

        # If input is username, convert it to actual email
        try:
            user = User.objects.get(username__iexact=value)
            return user.email
        except User.DoesNotExist:
            return value
        
class UsernameOrEmailAuthenticationForm(AuthenticationForm):

    def clean_username(self):
        username = self.cleaned_data.get("username")

        # If input looks like email
        if "@" in username:
            try:
                user = User.objects.get(email__iexact=username)
                return user.username
            except User.DoesNotExist:
                return username

        return username