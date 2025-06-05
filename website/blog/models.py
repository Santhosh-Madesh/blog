from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    pfp = models.ImageField(upload_to="media/",default="media/default.jpg",null=True,blank=True)
    name = models.CharField()
    age = models.IntegerField()
    instagram_id = models.CharField()
    bio = models.CharField()
    
class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=date.today())
    title = models.CharField()
    introduction = models.CharField()
    content = models.CharField()
    conclusion = models.CharField()