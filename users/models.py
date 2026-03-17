from django.db import models
from django.contrib.auth.models import User
import uuid
from django.forms import ModelForm
from django import forms



# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=200,blank=True,null=True)
    email=models.EmailField(max_length=500,blank=True,null=True)
    views = models.IntegerField(default=0, editable=False)
    short_intro=models.CharField(max_length=200,blank=True,null=True)
    bio=models.TextField(blank=True,null=True)
    profile_image=models.ImageField(null=True,blank=True,upload_to='ProfileImages/',default='default.jpg')
    social_github=models.CharField(max_length=200,blank=True,null=True)
    social_linkedin=models.CharField(max_length=200,blank=True,null=True)
    social_instagram=models.CharField(max_length=200,blank=True,null=True)
    social_leetcode=models.CharField(max_length=200,blank=True,null=True)
    social_hackerrank=models.CharField(max_length=200,blank=True,null=True)
    portfolio=models.CharField(max_length=200,blank=True,null=True)
    created=models.DateTimeField(auto_now_add=True)
    role=models.CharField(max_length=50,blank=True,null=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    STATUS_CHOICES = [
        ('employed', 'Employed'),
        ('open', 'Open to Work'),
        ('hiring', 'Hiring'),
        ('opportunity', 'Open to Opportunities'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='employed'
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exclude(id=self.instance.user.id).exists():
            raise forms.ValidationError("Username already taken")

        return username
    
    def __str__(self):
        return str(self.user)
    
    
    
class Skill(models.Model):
    owner=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=200, blank=True,null=True)
    description=models.TextField(null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    
    def __str__(self):
        return str(self.name)