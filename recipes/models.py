from django.db import models
from django.conf import settings

class Recipe(models.Model):
    title = models.TextField()
    description = models.TextField()
    cuisine = models.TextField()
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ForeignKey('recipes.Recipe', related_name='comments', on_delete=models.CASCADE)
    message = models.TextField(null=True)
