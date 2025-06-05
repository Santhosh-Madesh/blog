from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostModelForm, ProfileModelForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Posts, Profile
from django.core.paginator import Paginator

@login_required
def home(request):
    posts = Posts.objects.all().order_by("date")
    page = Paginator(posts,2)

    page_number = request.GET.get("page")
    page_obj = page.get_page(page_number)
    return render(request,"blog/index.html",{"page_obj":page_obj})


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