from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Podcast(models.Model):
    audio = models.FileField(upload_to='podcast_audios', max_length=100)    
    title = models.CharField(max_length=60)
    description = models.TextField()
    length = models.FloatField(blank=True)
    audio_uploader = models.ForeignKey(User,related_name='podcasts', null = True, on_delete= models.SET_NULL)
    speaker = models.ForeignKey(User, related_name= 'speaker', null=True, on_delete= models.SET_NULL, blank=True)
    date_published = models.DateField(auto_now_add=True)


class Saved_podcasts(models.Model):
    podcast = models.ManyToManyField(Podcast, related_name='is_saved')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_pods')
    

