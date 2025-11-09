from django.contrib import admin
from .models import Post, Author
# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('username', 'bio', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'first_name','last_name', 'email')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'published')
    search_fields = ('title', 'author__username', 'author__first_name', 'author__last_name')
    list_filter = ('published', 'author')
