from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post, Author
from .forms import PostForm
# Create your views here.

# View all posts
def post_list(request):
    # select * from posts => Post.objects.all() "ORM"
    All_posts = Post.objects.all() 
    context = {
        'All_posts': All_posts,
        'today': timezone.now().date(),
        'total_posts': All_posts.count(),
    }
    return render(request, 'blog/post_list.html', context)

# View single post detail
def post_detail(request, post_id):
    # select * from posts where id = post_id
    post = Post.objects.get(id=post_id)
    context = {
        'post': post,
        'reading_time': len(post.content.split()) // 100 + 1,  # words per minute
    }
    return render(request, 'blog/post_detail.html', context)

# Create a new post view
# @login_required
def post_create(request):
    # Get or create author for current user
    author, created = Author.objects.get_or_create(id=request.user.id)
    
    if request.method == 'POST': # if form is submitted
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = author
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    
    context = {
        'form': form,
        'title': 'Create Post',
    }
    return render(request, 'blog/post_form.html', context)