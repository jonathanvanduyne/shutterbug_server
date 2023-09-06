from django.db import models

class Post(models.Model):
    shutterbug_user = models.ForeignKey("ShutterbugUser", on_delete=models.CASCADE, related_name="author_of_post")
    title = models.CharField(max_length=100)
    image_url = models.CharField(max_length=10000)
    content = models.CharField(max_length=300)
    published_on = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="category_of_post")
    approved = models.BooleanField(default=True)
    flagged = models.BooleanField(default=False)
    tags = models.ManyToManyField("Tag", through="PostTag", related_name="post_tag")
    reactions = models.ManyToManyField("Reaction", through="PostReaction", related_name="post_reaction")