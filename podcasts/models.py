from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Podcast(models.Model):
    audio = models.FileField(upload_to='podcast_audios', max_length=100)     
    title = models.CharField(max_length=60)
    description = models.TextField()
    length = models.FloatField()  # Removed blank=True as it should be required
    audio_uploader = models.ForeignKey(User, related_name='podcasts', null=True, on_delete=models.SET_NULL)
    speaker = models.ForeignKey(User, related_name='speaker_podcasts', null=True, on_delete=models.SET_NULL, blank=True)
    date_published = models.DateTimeField(auto_now_add=True)  # Changed to DateTimeField for more precision

    def __str__(self):
        return self.title 

class SavedPodcast(models.Model):  # Changed class name to follow Python naming conventions
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_podcasts')
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name='saved_by')
    date_saved = models.DateTimeField(auto_now_add=True)  # Changed to use timezone.now without parentheses

    class Meta:
        unique_together = ('user', 'podcast')

    def __str__(self):
        return f"{self.user.username} saved {self.podcast.title}"    