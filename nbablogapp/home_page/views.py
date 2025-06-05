from nbablogapp.models import *
from django.shortcuts import render, redirect
from django.contrib.sites.models import *
from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST

@login_required(login_url='home_page:login')
def home(request):
    if request.method == 'POST':
        post_content = request.POST.get('post_content')
        post = Post.objects.create(
            content=post_content,
            author=request.user
        )
        post.save()
        return redirect('home_page:home')
    
    user = request.user
    posts = Post.objects.filter(Q(author__in=user.following.all()) | Q(author=user)).order_by('-date_posted')
    page = request.GET.get('page')
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page)
    for post in page_obj:
        post.is_liked = user.liked_post(post)
        post.is_reposted = user.reposted_post(post)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = ''
        for post in page_obj:
            post.is_liked = user.liked_post(post)
            post.is_reposted = user.reposted_post(post)
            html += render(request, 'home_page/widgets/post.html', {'post': post}).content.decode()
        return JsonResponse({'html': html, 'has_next': page_obj.has_next()})
    return render(request, 'home_page/home.html', {'page_obj': page_obj})

@require_POST
@login_required(login_url='home_page:login')
def interact_post(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        post_id = request.POST.get('post_id')
        action = request.POST.get('action')
        post = Post.objects.get(id=post_id)
        new_count = 0
        
        if action == 'like':
            if not request.user.liked_post(post):
                post.likes.create(user=request.user)
            else:
                post.likes.filter(user=request.user).delete()
            new_count = post.get_like_count()
        
        elif action == 'repost':
            if not request.user.reposted_post(post):
                post.reposts.create(user=request.user)
            else:
                post.reposts.filter(user=request.user).delete()
            new_count = post.get_repost_count()
        
        # elif action == 'reply':
        #     reply_content = request.POST.get('reply_content')
        #     reply = Reply.objects.create(
        #         content=reply_content,
        #         author=request.user,
        #         parent_post=post
        #     )
        #     reply.save()
        
        return JsonResponse({'success': True, 'new_count': new_count})
    
    return JsonResponse({'success': False, 'error': 'Error code 400'}, status=400)

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
