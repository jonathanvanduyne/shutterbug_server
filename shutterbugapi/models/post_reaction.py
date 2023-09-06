from django.db import models

class PostReaction(models.Model):
    shutterbug_user = models.ForeignKey("ShutterbugUser", on_delete=models.CASCADE, related_name="shutterbug_user_reaction")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="reaction_on_post")
    reaction = models.ForeignKey("Reaction", on_delete=models.CASCADE, related_name="reaction_on_post")