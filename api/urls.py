from django.urls import path
from .views import post_list

urlpatterns = [
    path('all_posts/', post_list, name='api_post_list'),
    # path('posts/create/', post_create, name='api_post_create'),
]