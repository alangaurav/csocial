from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Post, Profile, Company
from django.contrib.auth.models import User

class UserAndProfileCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileUpdateForm(forms.ModelForm):
    profile_image = forms.ImageField(required=False)
    #description = forms.CharField(widget=forms.Textarea, required=False)
    #company = forms.ModelChoiceField(queryset=Company.objects.all(), required=False)
    class Meta:
        model = Profile
        fields = ['profile_image']

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    class Meta:
        model = User
        fields =['first_name', 'last_name']

class CompanyUpdateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['location']

class LoginForm(forms.Form):
    class Meta:
        model = Profile
        fields = ['user']

class PostForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    tags = forms.CharField(max_length=500, required=False)
    class Meta:
        model = Post
        fields = ['title', 'description', 'tags','image']