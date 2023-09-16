from django.db import models

class DirectMessage(models.Model):
    sender = models.ForeignKey("ShutterbugUser", on_delete=models.CASCADE, related_name="sender")
    recipient = models.ForeignKey("ShutterbugUser", on_delete=models.CASCADE, related_name="recipient")
    content = models.CharField(max_length=300)
    created_on = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)