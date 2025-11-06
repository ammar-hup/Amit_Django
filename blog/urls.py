from django.urls import path
from .views import post_list, post_detail

urlpatterns = [
    path('all_posts/', post_list, name='post_list'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
]

# http://127.0.0.1:8000/blog/all_posts/
# post_id = primary key
