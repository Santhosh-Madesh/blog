from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostModelForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Posts

@login_required
def home(request):
    posts = Posts.objects.all()
    context = []
    for data in posts:
        context.append(
            {
            "date":data.date,
            "title":data.title,
            "introduction":data.introduction,
            "content":data.content,
            "conclusion":data.conclusion,
            }
        )
    return render(request,"blog/index.html",{"context":context})


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
