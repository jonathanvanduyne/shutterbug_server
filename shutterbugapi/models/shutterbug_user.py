from django.db import models

class ShutterbugUser(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE)
    bio = models.CharField(max_length=300, default="No bio provided")
    is_active = models.BooleanField(default=True)
    profile_image_url = models.CharField(max_length=300, default="No profile image provided")
    created_on = models.DateTimeField(auto_now_add=True)
