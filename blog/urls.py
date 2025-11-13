from django.urls import path
from .views import *

urlpatterns = [
    path('all_posts/', post_list, name='post_list'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('post_create/', post_create, name='post_create'),
]

# http://127.0.0.1:8000/blog/all_posts/
# post_id = primary key
