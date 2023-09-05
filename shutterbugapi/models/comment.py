from django.db import models

class Comment(models.Model):
    shutterbug_user = models.ForeignKey("ShutterbugUser", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    published_on = models.DateTimeField(auto_now_add=True)
    flagged = models.BooleanField(default=False)
    approved = models.BooleanField(default=True)