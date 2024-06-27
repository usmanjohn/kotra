from django.db import models
from django.contrib.auth.models import User
from topics.models import Topic, Answer, Upvoter, UpvoterAnswer
from django.db.models import Count, Q


    



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    image = models.ImageField(upload_to='profile_pics', default='profile_pics/default.png')
    bio = models.CharField(max_length=150)
    instagram_url = models.URLField(blank=True, null=True, default='#')
    facebook_url = models.URLField(blank=True, null=True, default='#')
    twitter_url = models.URLField(blank=True, null=True, default='#')
    youtube_url = models.URLField(blank=True, null=True, default='#')
    other_url = models.URLField(blank=True, null=True, default='#')
    link_image = models.ImageField(upload_to='links', default='links/personal_profile.png')
    

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
        if gains >= 10 and gains <50:
            badge = 'Conductor'
        
        if gains >= 50 and gains <200:
            badge = 'Influencer'
        
        if gains >= 200:
            badge = 'Driver'
        return badge
         
        
