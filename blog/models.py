from django.db import models
from django.contrib.auth.models import AbstractUser

class Author(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profile_pic = models.ImageField(upload_to='media/profile_pics/', blank=True, null=True) # optional field

    def __str__(self):
        return self.get_full_name() or self.username
    class Meta:
        verbose_name = 'author'
        verbose_name_plural = 'authors'

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)
    comments = models.TextField(blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE,related_name='posts') # safe delete
    image = models.ImageField(upload_to='media/post_images/', blank=True, null=True) # optional field

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
