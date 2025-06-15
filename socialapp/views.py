from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Comment, Like, Follow
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'socialapp/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'socialapp/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'socialapp/home.html', {'posts': posts})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, author=request.user, content=content)
            return redirect('post_detail', post_id=post.id)  

    comments = Comment.objects.filter(post=post).order_by('-created_at')

    has_liked = post.like_set.filter(user=request.user).exists()

    context = {
        'post': post,
        'comments': comments,
        'has_liked': has_liked,
    }
    return render(request, 'socialapp/post_detail.html', context)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    
    if not created:
        like.delete()
        messages.success(request, "Vous avez retiré votre like.")
    else:
        messages.success(request, "Vous avez liké ce post.")
    
    return redirect('post_detail', post_id=post_id)
    
@login_required
def follow_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    
    if request.user == target_user:
        messages.warning(request, "Vous ne pouvez pas vous suivre vous-même.")
        return redirect('home')

    existing_follow = Follow.objects.filter(follower=request.user, following=target_user)
    
    if existing_follow.exists():
        existing_follow.delete()
        messages.success(request, "Vous ne suivez plus cet utilisateur.")
    else:
        Follow.objects.create(follower=request.user, following=target_user)
        messages.success(request, "Vous suivez maintenant cet utilisateur.")
    
    return redirect('profile', user_id=target_user.id)  # Optionnel : redirige vers le profil de l’utilisateur suivi

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'socialapp/create_post.html', {'form': form})
@login_required
def profile_view(request, user_id):
    user_profile = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(author=user_profile).order_by('-created_at')

    is_following = False
    if request.user != user_profile:
        is_following = Follow.objects.filter(follower=request.user, following=user_profile).exists()

    context = {
        'user_profile': user_profile,
        'posts': posts,
        'is_following': is_following
    }
    return render(request, 'socialapp/profile.html', context)
@login_required
def user_list_view(request):
    query = request.GET.get('q')
    users = User.objects.exclude(id=request.user.id)  

    if query:
        users = users.filter(username__icontains=query)

    following_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)

    return render(request, 'socialapp/user_list.html', {
        'users': users,
        'following_ids': following_ids,
        'query': query
    })
@login_required
def feed_view(request):
    followed_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)

    posts = Post.objects.filter(author__in=followed_users).order_by('-created_at')

    return render(request, 'socialapp/feed.html', {'posts': posts})





