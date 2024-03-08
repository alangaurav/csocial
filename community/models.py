from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=20)
    domain = models.CharField(max_length=50)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    company = models.ForeignKey(Company, blank=True, on_delete=models.CASCADE, null=True)
    class Meta:
        permissions = (
                ("can_view_data", "Can view sensitive data"),
                ("can_edit_data", "Can edit sensitive data"),
            )

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

class Post(models.Model):
    created_on = models.DateTimeField(default=timezone.now, editable=False)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images', blank=True, null=True)
    description = models.TextField(blank=True)
    title = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag)
    location = models.TextField(blank=True)

class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now, editable=False)
    description = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')