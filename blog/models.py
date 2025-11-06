from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)
    comments = models.TextField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
