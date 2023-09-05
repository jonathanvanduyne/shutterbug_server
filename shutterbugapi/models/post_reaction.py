from django.db import models

class PostReaction(models.Model):
    shutterbug_user = models.ForeignKey("ShutterbugUser", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    reaction = models.ForeignKey("Reaction", on_delete=models.CASCADE)