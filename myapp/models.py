from django.db import models

# Create your models here.
class Song(models.Model):
    song_name = models.TextField(default="song")
    song_num = models.TextField(default="32410")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "songlist"
