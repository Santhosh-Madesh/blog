from django import forms
from .models import Profile, Posts
from django.contrib.auth.models import User

class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields=["pfp","name","age","instagram_id","bio"]

class PostModelForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ["date","title","introduction","content","conclusion"]

class SignUpForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())