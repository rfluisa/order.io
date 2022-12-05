from django.contrib.auth.models import User
from django.db import models


class Music(models.Model):
    title = models.CharField(max_length=64, verbose_name="Título")
    artist = models.CharField(max_length=64, verbose_name="Artista")
    url = models.URLField()

    def __str__(self):
        return f"{self.artist} - {self.title}"


class Order(models.Model):
    artist = models.ForeignKey(User, on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    tab = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.music} - {self.artist}"
