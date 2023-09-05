from django.db import models

class tag(models.Model):
    label = models.CharField(max_length=100)