from django.db import models
from first_django import settings

class Author(models.Model):
    # username, password, email, first_name, last_name and bio , profile_picture are in CustomUser model
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username

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
