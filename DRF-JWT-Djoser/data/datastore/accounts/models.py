from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# -------------------------
# Custom User Model
# -------------------------
class CustomUser(AbstractUser):
    """
    Minimal custom user model for authentication and identity.
    """
    # Display users phone number and future development feature
    # So when we implement sms verification we can inform the users
    phone = models.CharField(max_length=20, blank=True, null=True)
    def __str__(self):
        return self.username

# -------------------------
# User Profile Model
# -------------------------
class Profile(models.Model):
    """
    Extended user profile model for personal info.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"