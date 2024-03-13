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
            return JsonResponse({'message': 'Valid Credentials', 'invalid': 'False'})
        else:
            return JsonResponse({'message': 'Invalid Credentials', 'invalid': 'True'})
    else:
        return render(request, 'login_form.html')

def signup_view(request):
    if request.method == 'POST':
        user_profile_form = UserAndProfileCreationForm(request.POST)
        if user_profile_form.is_valid():
            checkEmail = User.objects.get(email=user_profile_form.cleaned_data['email'])
            if checkEmail is not None:
                return JsonResponse({'message': 'Email already in use!', 'invalid': 'True'})
            else:
                user = user_profile_form.save()  # Save User object
                company = Company.objects.get(domain=user_profile_form.cleaned_data['email'].split('@')[-1])
                profile = Profile(
                    user=user,
                    #date_of_birth=user_profile_form.cleaned_data['date_of_birth'],
                    #profile_image=user_profile_form.cleaned_data['profile_image'],
                    #description=user_profile_form.cleaned_data['description'],
                    company = company
                )
                profile.save()
                return JsonResponse({'message': 'Valid Credentials', 'invalid': 'False'})
        else:
            return JsonResponse({'message': user_profile_form.errors.as_text(), 'invalid': 'True'})
    else:
        return render(request, 'signup.html')

@login_required
def posts_view(request):
    if request.method == 'GET':
        if request.GET:
            filter = list(request.GET.keys())[0]
        else:
            filter = None
        if filter == 'category':
            category = request.GET.get('category')
            posts = Post.objects.filter(category=category).order_by('-created_on')
        elif filter == 'tag':
            tagFilter = request.GET.get('tag')
            posts = Post.objects.filter(tags__name=tagFilter).distinct().order_by('-created_on')
        elif filter == 'tagcategory':
            category = request.GET.get('tagcategory')
            posts = Post.objects.filter(tags__category=category).distinct().order_by('-created_on')
        else:
            posts = Post.objects.all().order_by('-created_on')
    else:
        filter = request.POST['search']
        posts = Post.objects.filter(title__icontains=filter) | Post.objects.filter(description__icontains=filter) | Post.objects.filter(author__user__username__icontains=filter) | Post.objects.filter(comments__description__icontains=filter) | Post.objects.filter(tags__name__icontains=filter)
        posts = posts.distinct()
    
    return render(request, 'posts.html', {'posts': posts})

@login_required
def profile_view(request):
    profileid = request.GET.get('profile')
    if profileid:
        profile = Profile.objects.get(id=profileid)
    else:
        profile = Profile.objects.get(user=request.user)
    posts = Post.objects.filter(author=profile).order_by('-created_on')
    return render(request, 'profile.html', {'profile': profile, 'posts': posts})

@login_required
def profile_settings(request):
    if request.method == "GET":
        profile = Profile.objects.get(user=request.user)
        return render(request, 'user-settings.html', {'profile': profile})
    else:
        profile_update_form = ProfileUpdateForm(request.POST)
        if profile_update_form.is_valid():
            updateProfile = Profile.objects.get(user=request.user)
            updateUser = updateProfile.user
            if profile_update_form.cleaned_data['first_name']:
                updateUser.first_name = profile_update_form.cleaned_data['first_name']
                updateUser.save(update_fields=['first_name'])
            if profile_update_form.cleaned_data['last_name']:
                updateUser.last_name = profile_update_form.cleaned_data['last_name']
                updateUser.save(update_fields=['last_name'])
            updateUser = updateUser.refresh_from_db()
            if profile_update_form.cleaned_data['profile_image']:
                updateProfile.profile_image = profile_update_form.cleaned_data['profile_image']
                updateProfile.save(update_fields=['profile_image'])
            if  profile_update_form.cleaned_data['description']:
                updateProfile.description = profile_update_form.cleaned_data['description']
                updateProfile.save(update_fields=['description'])
            updateProfile.refresh_from_db()
            return render(request, 'user-settings.html', {'profile': updateProfile})
        else:
            return JsonResponse({'message': profile_update_form.errors.as_text})

@login_required
def newpost(request):
    if request.method == 'GET':
        return render(request, 'new_post.html')
    elif request.method == 'POST':
        postform = PostForm(request.POST, request.FILES)
        if postform.is_valid():
            profile = Profile.objects.get(user=request.user)
            post = Post(
                author= profile,
                title = postform.cleaned_data['title'],
                description = postform.cleaned_data['description'],
                image = postform.cleaned_data['image'],
                location = profile.company.location,
                category = postform.cleaned_data['category']
            )
            post.save()
            tagCategory = request.POST['tag-category']
            tagList = request.POST['tags'].split(' ')
            for tag in tagList:
                 try:
                     newtag = Tag.objects.create(name=tag, category=tagCategory)
                     newtag.save()
                     post.tags.add(newtag)
                 except:
                     post.tags.add(Tag.objects.get(name=tag))
            return JsonResponse({'message': 'Post created successfully!', 'invalid': 'False'})
        else:
            return JsonResponse({'message': 'Post could not be created!', 'invalid': 'True'})

@login_required
def singlePost(request):
    if request.method == 'GET':
        postid = request.GET.get('post')
        post = Post.objects.get(id=postid)
        comments = Comment.objects.filter(post=post)
        return render(request, 'singlepost.html', {'post': post, 'comments': comments})
    
@login_required
def newcomment(request):
    comments = request.POST['newcomment']
    postid = request.GET.get('post')
    comment = Comment(
        author = Profile.objects.get(user=request.user),
        description = comments,
        post = Post.objects.get(id=postid)
    )
    comment.save()
    return JsonResponse({'message': 'Comments added!', 'invalid': 'False'})
    
def logout_view(request):
    logout(request)
    return redirect('login')

