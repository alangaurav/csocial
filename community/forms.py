from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import *
from django.contrib.auth.models import User
from django.core.validators import EmailValidator

class UserAndProfileCreationForm(UserCreationForm):
    domains = Company.objects.values_list('domain')
    email = forms.EmailField(validators=[EmailValidator(allowlist=domains)])
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
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control'}), required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control'}), required=True)
    category = forms.ChoiceField(choices=Post.categories, widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Post
        fields = ['title', 'description', 'category', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['description']