from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pfp = models.ImageField(default="default.jpg",null=True,blank=True)
    name = models.CharField()
    age = models.IntegerField()
    instagram_id = models.CharField()
    bio = models.CharField(models.TextField())
    
class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    title = models.CharField()
    introduction = models.CharField(models.TextField())
    content = models.CharField(models.TextField())
    conclusion = models.CharField(models.TextField())