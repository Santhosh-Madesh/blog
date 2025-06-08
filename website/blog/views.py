from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import PostModelForm, ProfileModelForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Posts, Profile
from django.core.paginator import Paginator
from django.views import View
from django.views.generic import ListView, DetailView, FormView,  DeleteView
from django.urls import reverse_lazy


@method_decorator(login_required, name="dispatch")
class IndexListView(ListView):
    model = Posts
    template_name = "blog/index.html"
    context_object_name = "blog_posts"


@method_decorator(login_required, name="dispatch")
class BlogCreationFormView(FormView):
    template_name = "blog/blog_creation.html"
    form_class = PostModelForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        
        form.instance.user = self.request.user
        form.save()

        return super().form_valid(form)


@method_decorator(login_required,name="dispatch")
class MyBlogListView(ListView):
    template_name = "blog/my_blogs.html"

    def get(self, request):
        user = request.user
        context = Posts.objects.filter(user = user)
        return render(request,self.template_name,{"context":context})
        

@login_required
def delete(request,pk):
    post = Posts.objects.get(id=pk)
    post.delete()
    messages.success(request,"Post deleted successfully!")
    return redirect("my_blogs")

@method_decorator(login_required, name="dispatch")
class DeleteBlogView(DeleteView):
    model = Posts
    success_url = reverse_lazy("my_blogs")
    template_name = "blog/blog_deletion_confirmation.html"


@method_decorator(login_required, name="dispatch")
class ViewBlogDetailView(DetailView):
    model = Posts
    template_name = "blog/view_blog.html"
    context_object_name = "post"

    def get_object(self, queryset = None):
        pk = self.kwargs.get("pk")
        return Posts.objects.get(id = pk)

@login_required
def update_blog(request,pk):
    if request.method == "POST":
        form = PostModelForm(request.POST)
        if form.is_valid():
            post = Posts.objects.get(id=pk)
            post.title = form.cleaned_data["title"]
            post.introduction = form.cleaned_data["introduction"]
            post.content = form.cleaned_data["content"]
            post.conclusion = form.cleaned_data["conclusion"]
            post.save()
            
            messages.success(request,"Blog updated successfully!")
            return redirect("my_blogs")
        
    post = Posts.objects.get(id = pk)
    form = PostModelForm(initial={"title":post.title,"introduction":post.introduction,"content":post.content,"conclusion":post.conclusion})
    return render(request,"blog/blog_update.html",{"form":form,"pk":pk})
    
@login_required
def dashboard(request):
    if request.method == "POST":
        form = ProfileModelForm(request.POST,request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request,"Dashboard has been updated successfully!")
            return redirect("dashboard")
    user = request.user
    profile = Profile.objects.filter(user=user)
    if profile:
        return render(request,"blog/dashboard.html",{"context":profile})
    else:
        form = ProfileModelForm()
        return render(request,"blog/dashboard.html",{"form":form})
    
@login_required
def update_dashboard(request):
    if request.method == "POST":
        form = ProfileModelForm(request.POST, request.FILES)
        if form.is_valid():
            profile = Profile.objects.get(user=request.user)
            profile.pfp = request.FILES["pfp"]
            profile.name = form.cleaned_data["name"]
            profile.age = form.cleaned_data["age"]
            profile.instagram_id = form.cleaned_data["instagram_id"]
            profile.bio = form.cleaned_data["bio"]
            profile.save()
            messages.success(request,"Dashboard updated successfully!")
            return redirect("dashboard")
    profile = Profile.objects.filter(user=request.user)
    if profile:
        for data in profile:
            form = ProfileModelForm(
                initial={
                    "pfp":data.pfp,
                    "name":data.name,
                    "age":data.age,
                    "instagram_id":data.instagram_id,
                    "bio":data.bio,
                }
            )
        return render(request,"blog/update_dashboard.html",{"form":form})
    else:
        messages.error(request,"You do not have a dashboard to update, Create one.")
        return redirect("dashboard")
    
@login_required
def search(request):
    search_data = request.GET["search"]
    try:
        user = User.objects.get(username = search_data)
    except User.DoesNotExist:
        messages.error(request,"No such user exists!")
        return redirect("home")
    
    profile = Profile.objects.filter(user=user)
    if profile:
        return render(request,"blog/user_search.html",{"context":profile})
    else:
        return render(request,"blog/user_search.html",{"user":user})
    