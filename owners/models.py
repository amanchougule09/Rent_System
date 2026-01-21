from django.db import models
from accounts.models import UserProfile

class Owner(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Owner ({self.user.mobile})"
    

