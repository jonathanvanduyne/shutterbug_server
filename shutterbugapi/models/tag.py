from django.db import models

class Tag(models.Model):
    label = models.CharField(max_length=100)
    posts = models.ManyToManyField("Post", through="PostTag", related_name="tags_on_post")