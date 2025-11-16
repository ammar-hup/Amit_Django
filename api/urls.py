from django.urls import path
from .views import (PostListCBV, post_list,post_detail,post_create,post_update,post_delete)

urlpatterns = [
    path('all_posts/', post_list, name='api_post_list'),
    path('post/<int:post_id>/', post_detail, name='api_post_detail'),
    path('posts/create/', post_create, name='api_post_create'),
    path('post/<int:post_id>/update/', post_update, name='api_post_update'),
    path('post/<int:post_id>/delete/', post_delete, name='api_post_delete'),
    path('cbv/posts/', PostListCBV.as_view(), name='api_cbv_post_list'),
]