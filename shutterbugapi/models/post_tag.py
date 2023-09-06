from django.db import models

class PostTag(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="tagged_post")
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE, related_name="tagged_tag")