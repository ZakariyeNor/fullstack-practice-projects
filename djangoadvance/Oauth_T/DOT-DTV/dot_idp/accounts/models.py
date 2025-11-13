from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_ADMIN = "admin"
    ROLE_LAWYER = "lawyer"
    ROLE_GUEST = "guest"
    
    ROLE_CHOICES = [
        (ROLE_ADMIN, "Admin"),
        (ROLE_LAWYER, "Lawyer"),
        (ROLE_GUEST, "Guest"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_GUEST)
    
    def is_admin(self):
        return self.role == self.ROLE_ADMIN
    
    def is_lawyer(self):
        return self.role == self.ROLE_LAWYER
    
    def is_guest(self):
        return self.role == self.ROLE_GUEST