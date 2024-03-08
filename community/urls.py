from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.posts_view, name='posts'),
    path('login/', views.my_login_view, name='login'),
    path('posts/', views.posts_view, name='posts'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('user-settings/', views.profile_settings, name='settings'),
    path('logout/', views.logout_view, name='logout'),
    path('newpost/', views.newpost, name="new_post"),
    path('singlepost/', views.singlePost, name='singlepost')
]