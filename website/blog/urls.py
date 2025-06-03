from django.urls import path
from . import views, auth

urlpatterns=[
    path("",views.home,name="home"),
    path("signup/",auth.signup,name="signup"),
    path("login/",auth.login_page,name="login"),
    path("logout/",auth.logout_page,name="logout"),
]