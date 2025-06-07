from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import PostModelForm, ProfileModelForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Posts, Profile
from django.core.paginator import Paginator
from django.views import View
from django.views.generic import ListView


@method_decorator(login_required, name="dispatch")
class IndexListView(ListView):
    model = Posts
    template_name = "blog/index.html"
    context_object_name = "blog_posts"


@login_required
def blog_creation(request):
    if request.method == "POST":
        form = PostModelForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request,"New Blog has been created Successfully")
            return redirect("home")
        else:
            messages.error(request,"Invalid blog creation. Try Again!")
            return redirect("blog_creation")
            
    form = PostModelForm()
    return render(request,"blog/blog_creation.html",{"form":form})

@login_required
def my_blogs(request):
    user = request.user
    posts = Posts.objects.filter(user=user)
    context = []
    for data in posts:
        context.append(
            {
                "pk":data.id,
                "title":data.title,
            }
            )
    return render(request,"blog/my_blogs.html",{"context":context})

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

@login_required
def view_blog(request,pk):
    post = Posts.objects.get(id=pk)
    context = {
        "title":post.title,
        "date":post.date,
        "introduction":post.introduction,
        "content":post.content,
        "conclusion":post.conclusion,
    }
    return render(request,"blog/view_blog.html",context)

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
    