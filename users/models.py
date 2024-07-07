from django.db import models
from django.contrib.auth.models import User
from topics.models import Topic, Answer, Upvoter, UpvoterAnswer
from django.db.models import Count, Q
 
from django.utils import timezone
    
from django.contrib.auth.models import AbstractUser


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    is_email_verified = models.BooleanField(default=False)
    image = models.ImageField(upload_to='profile_pics', default='profile_pics/default.png')
    bio = models.CharField(max_length=300, default='I did not write a bio yet')
    instagram_url = models.URLField(blank=True, null=True, default='https://instagram.com/')
    facebook_url = models.URLField(blank=True, null=True, default='https://facebook.com/')
    twitter_url = models.URLField(blank=True, null=True, default='https://x.com/')
    youtube_url = models.URLField(blank=True, null=True, default='https://www.youtube.com/')
    other_url = models.URLField(blank=True, null=True, default='https://www.youtube.com/')
    link_image = models.ImageField(upload_to='links', default='links/personal_profile.png')
    date = models.DateField(auto_now_add=True)
    

    def __str__(self) -> str:
        return f'{self.user.username} Profile' 
    @property
    def total_gains(self):
        topics_upvotes = Topic.objects.filter(
            topic_author=self.user
        ).annotate(
            upvotes_count=Count('question', filter=Q(question__vote_type=1))
        ).aggregate(total_upvotes=models.Sum('upvotes_count'))['total_upvotes'] or 0

        answers_upvotes = Answer.objects.filter(
            answer_author=self.user
        ).annotate(
            upvotes_count=Count('votes', filter=Q(votes__vote_type=1))
        ).aggregate(total_upvotes=models.Sum('upvotes_count'))['total_upvotes'] or 0

        return topics_upvotes + answers_upvotes
    @property
    def badge_status(self):
        gains = self.total_gains
        badge = 'None'
        if gains == 0:
            badge = 'Observer'
        if gains > 0 and gains < 10:
            badge = 'Passenger'
        if gains >= 10 and gains <30:
            badge = 'Conductor'
        
        if gains >= 30 and gains <50:
            badge = 'Influencer'
        
        if gains >= 50:
            badge = 'Driver'
        return badge
         
        
