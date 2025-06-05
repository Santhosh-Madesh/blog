from django.urls import path
from . import views, auth

urlpatterns=[
    path("",views.home,name="home"),
    path("blog_creation/",views.blog_creation,name="blog_creation"),
    path("my_blogs/",views.my_blogs,name="my_blogs"),
    path("delete_blog/<int:pk>",views.delete,name="delete"),
    path("view_blog/<int:pk>",views.view_blog,name="view_blog"),
    path("update_blog/<int:pk>",views.update_blog,name="blog_update"),
    path("signup/",auth.signup,name="signup"),
    path("login/",auth.login_page,name="login"),
    path("logout/",auth.logout_page,name="logout"),
]