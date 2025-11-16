from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    # username, password, email, first_name, last_name are already included
    # You can add additional fields here if needed
    activision_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=False)  # Inactive until email confirmed
    date_joined = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    