from django.urls import path
from . import views, auth
from .views import IndexListView, MyBlogListView, ViewBlogDetailView, BlogCreationFormView, DeleteBlogView, UpdateBlogView

urlpatterns=[
    path("",IndexListView.as_view(),name="home"),
    path("blog_creation/",BlogCreationFormView.as_view(),name="blog_creation"),
    path("my_blogs/",MyBlogListView.as_view(),name="my_blogs"),
    path("delete_blog/<int:pk>",DeleteBlogView.as_view(),name="delete"),
    path("view_blog/<int:pk>",ViewBlogDetailView.as_view(),name="view_blog"),
    path("update_blog/<int:pk>",UpdateBlogView.as_view(),name="blog_update"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path("dashboard_update/",views.update_dashboard,name="dashboard_update"),
    path("search/",views.search,name="search"),
    path("signup/",auth.signup,name="signup"),
    path("login/",auth.login_page,name="login"),
    path("logout/",auth.logout_page,name="logout"),
]