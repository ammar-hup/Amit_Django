from django.shortcuts import render
from django.utils import timezone
from .models import Post
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
