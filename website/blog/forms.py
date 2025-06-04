from django import forms
from .models import Profile, Posts
from django.contrib.auth.models import User

class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude=['user']
        widgets={
            'bio':forms.Textarea(),
        }

class PostModelForm(forms.ModelForm):
    class Meta:
        model = Posts
        exclude=["user","date"]
        widgets={
            'introduction':forms.Textarea(),
            'content':forms.Textarea(),
            'conclusion':forms.Textarea(),
        }

class SignUpForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())