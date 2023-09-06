from django.db import models
from django.contrib.auth.models import User

class ShutterbugUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=300, default="No bio provided")
    profile_image_url = models.CharField(max_length=300, default="No profile image provided")


    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"