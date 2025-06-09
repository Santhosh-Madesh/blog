from django.shortcuts import render,redirect
from .forms import SignUpForm,LoginForm
from django.contrib.auth import login,logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User(first_name=first_name,last_name=last_name,username=username,email=email)
            user.set_password(password)
            user.save()
            messages.success(request,"Signed up successfully!")
            return redirect("login")
        else:
            messages.error(request,"Invalid input")
            return render(request,"blog/signup.html",{"form":form})
    form = SignUpForm()
    return render(request,"blog/signup.html",{"form":form})

def login_page(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already logged in, please logout to login with a different account!")
        return redirect("home")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username,password=password)
            if user is None:
                messages.error(request,"Invalid credentials!")
                return render(request,"blog/login.html",{"form":form})
            else:
                login(request,user)
                messages.success(request,"Login successful!")
                return redirect("home")
    form = LoginForm()
    return render(request,"blog/login.html",{"form":form})

class LoginPageView(LoginView):
    redirect_authenticated_user = True
    template_name = "blog/login.html"

    def get_success_url(self):
        messages.success(self.request, "Login Successful!")
        return reverse_lazy("home")
    
    def form_invalid(self, form):
        messages.error(self.request, "Invalid login credentials")
        return super().form_invalid(form)
    

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out successfully!")
        return redirect("login")
    else:
        messages.error(request,"You are not logged in!")
        return redirect("login")