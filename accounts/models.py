from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    # username, password, email, first_name, last_name are already included
    # You can add additional fields here if needed
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    