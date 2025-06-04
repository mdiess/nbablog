from nbablogapp.models import *
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.contrib.sites.models import *
from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required(login_url='home_page:login')
def home(request):
    if request.method == 'POST':
        print(request.POST)
        post_content = request.POST.get('post_content')
        post = Post.objects.create(
            content=post_content,
            author=request.user
        )
        post.save()
        return redirect('home_page:home')
    user = User.objects.filter(pk=request.user.pk).first()
    posts = Post.objects.filter(
        Q(author__in=user.following.all()) | Q(author=user)
    ).order_by('-date_posted')
    return render(request, 'home_page/home.html', {'posts': posts})

def login(request):
    if request.user.is_authenticated:
        return redirect('home_page:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('home_page:home')
    
    return render(request, 'login.html')

@login_required(login_url='home_page:login')
def logout_view(request):
    logout(request)
    return redirect('home_page:login')
