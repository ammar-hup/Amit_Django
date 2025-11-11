from django.urls import path
from .views import *

urlpatterns = [
    path('all_posts/', post_list, name='post_list'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('post_create/', post_create, name='post_create'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]

# http://127.0.0.1:8000/blog/all_posts/
# post_id = primary key
