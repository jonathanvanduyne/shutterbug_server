from django.db import models

class PostReaction(models.Model):
    shutterbug_user = models.ForeignKey("ShutterbugUser", on_delete=models.CASCADE, related_name="post_reaction_author")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post_reaction")
    reaction = models.ForeignKey("Reaction", on_delete=models.CASCADE, related_name="post_reaction")