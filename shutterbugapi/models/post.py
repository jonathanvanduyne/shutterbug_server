from django.db import models

class Post(models.Model):
    shutterbug_user = models.ForeignKey("ShutterbugUser", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image_url = models.CharField(max_length=10000)
    content = models.CharField(max_length=300)
    published_on = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    approved = models.BooleanField(default=True)
    flagged = models.BooleanField(default=False)