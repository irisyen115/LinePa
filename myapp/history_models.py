from django.db import models

# Create your models here.
class History(models.Model):
    keyword = models.TextField(default="")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("keyword",)
        ordering = ['-updated_at']

