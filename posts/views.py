# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Post, Comment
from .forms import PostForm, CommentForm

def home(request):
    posts = Post.objects.select_related('user').prefetch_related('likes', 'comments').all()
    comment_form = CommentForm()
    return render(request, 'posts/home.html', {'posts': posts, 'comment_form': comment_form})

@login_required
@require_POST
def like_post(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    
    return JsonResponse({'likes_count': post.likes.count(), 'liked': liked})

@login_required
@require_POST
def add_comment(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        return JsonResponse({
            'status': 'success',
            'comment_id': comment.id,
            'user': comment.user.username,
            'content': comment.content,
            'created_at': comment.created_at.strftime('%b %d, %Y, %I:%M %p')
        })
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

@login_required
def share_post(request, post_id):
    original_post = get_object_or_404(Post, id=post_id)
    shared_content = f"Shared post from {original_post.user.username}: {original_post.content}"
    
    new_post = Post.objects.create(
        user=request.user,
        content=shared_content,
        image=original_post.image  # You might want to handle this differently
    )
    
    messages.success(request, 'Post shared successfully!')
    return redirect('home')

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('home')
    return render(request, 'posts/delete_post.html', {'post': post})

