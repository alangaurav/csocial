from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import Post, Profile, Tag, Comment, Company
from .forms import *
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import JsonResponse


def my_login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('posts')
        else:
            return render(request, 'login_form.html', {'invalid': True, 'error_message': 'Invalid Credentials'})
    else:
        return render(request, 'login_form.html')

def signup_view(request):
    if request.method == 'POST':
        user_profile_form = UserAndProfileCreationForm(request.POST)
        print("Check if form is valid:")
        print(user_profile_form.is_valid())
        if user_profile_form.is_valid():
            print("Form is valid")
            user = user_profile_form.save()  # Save User object
            profile = Profile(
                user=user,
                #date_of_birth=user_profile_form.cleaned_data['date_of_birth'],
                #profile_image=user_profile_form.cleaned_data['profile_image'],
                #description=user_profile_form.cleaned_data['description'],
                #company = user_profile_form.cleaned_data['company']
            )
            profile.save()
            #messages.success(request, f'Your account has been created. You can now log in!')
            return redirect('login')  # Replace 'login' with your login view name
    else:
        user_profile_form = UserAndProfileCreationForm()
    
    return render(request, 'signup.html')

@login_required
def posts_view(request):
   posts = Post.objects.all().order_by('-created_on')
   return render(request, 'posts.html', {'posts': posts})

@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    posts = Post.objects.filter(author=profile)
    return render(request, 'profile.html', {'profile': profile, 'posts': posts})

@login_required
def profile_settings(request):
    if request.method == "GET":
        profile = Profile.objects.get(user=request.user)
        return render(request, 'user-settings.html', {'profile': profile})
    else:
        user_update_form = UserUpdateForm(request.POST)
        profile_update_form = ProfileUpdateForm(request.POST)
        if user_update_form.is_valid() and profile_update_form.is_valid():
            updateUser = User.objects.get(id=request.user.id)
            updateUser.first_name = user_update_form.cleaned_data['first_name']
            updateUser.last_name = user_update_form.cleaned_data['last_name']
            updateUser.save(update_fields=['first_name', 'last_name'])
            updateUser.refresh_from_db()
            updateProfile = Profile.objects.get(user=request.user)
            updateProfile.profile_image = profile_update_form.cleaned_data['profile_image']
            updateProfile.user = updateUser
            updateProfile.save(update_fields=['profile_image', 'user'])
            updateProfile.refresh_from_db()
            return render(request, 'user-settings.html', {'profile': updateProfile})

@login_required
def newpost(request):
    if request.method == 'GET':
        return render(request, 'new_post.html')
    elif request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            profile = Profile.objects.get(user=request.user)
            post = Post(
                author= profile,
                title = form.cleaned_data['title'],
                description = form.cleaned_data['description'],
                image = form.cleaned_data['image'],
                location = profile.company.location
            )
            post.save()
            tagList = form.cleaned_data['tags'].split(' ')
            for tag in tagList:
                try:
                    newtag = Tag.objects.create(name=tag)
                    newtag.save()
                    post.tags.add(newtag)
                except:
                    post.tags.add(Tag.objects.get(name=tag))
            return JsonResponse({'message': 'Post created successfully!'})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    
    return redirect('posts')

@login_required
def singlePost(request):
    if request.method == 'GET':
        postid = request.GET.get('post')
        post = Post.objects.get(id=postid)
        comments = Comment.objects.filter(post=post)
        return render(request, 'singlepost.html', {'post': post, 'comments': comments})

def logout_view(request):
    logout(request)
    return redirect('login')

