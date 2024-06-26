from django.db import models
from django.contrib.auth.models import User
from django.contrib import messages
from django_ckeditor_5.fields import CKEditor5Field
from taggit.managers import TaggableManager
from django.db.models import Count, Q

# Create your models here.
class Topic(models.Model):
    Category_CHOICES = (
    ('Topik','Topik'),
    ('KIIP', 'KIIP'),
    ('Daily','Daily'),
    ('Other','Other')
)

    topic_author = models.ForeignKey(User, related_name='topic_auth',on_delete=models.CASCADE)
    topic_title = models.CharField(max_length=150)
    topic_body = CKEditor5Field('Text', config_name='extends')
    hashtag = TaggableManager(blank=True)
    topic_hashtag = models.CharField(max_length=50)
    topic_category = models.CharField(choices=Category_CHOICES, default='Topik', max_length=15)
    topic_pub_date = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.topic_title
    
    def gains(self):
        # This property will return the count of upvotes for this particular topic instance
        return Upvoter.objects.filter(topic=self, vote_type=1).count()

class SavedTopic(models.Model): 
    user = models.ForeignKey(User, related_name='saved_topics', on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, related_name='saved_by_users', on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'topic')

    def __str__(self) -> str:
        return self.topic.title  # Assuming 'title' is a field in the Topic model

    @property
    def upvotes(self):
        return self.topic.question.filter(vote_type=1).count()
    @property
    def answers(self):
        return self.topic.answer.count()

            
        #saved_topic.upvotes = Upvoter.objects.filter(topic=saved_topic.topic, vote_type=1).count()
        #saved_topic.answers = Answer.objects.filter(topic_parent = saved_topic.topic).count()
            

class Answer(models.Model):
    answer_author = models.ForeignKey(User, related_name= 'answer_auth', on_delete=models.CASCADE )
    topic_parent = models.ForeignKey(Topic, related_name='answer', on_delete=models.CASCADE)
    answer_body = models.TextField()
    answer_pub_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.answer_body
    def gains(self):
        # This property will return the count of upvotes for this particular topic instance
        return UpvoterAnswer.objects.filter(answer=self, vote_type=1).count()

    

class Upvoter(models.Model):
    vote_choices = ((1,'upvote' ), (-1, 'downvote'))

    topic = models.ForeignKey(Topic, related_name='question', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.SmallIntegerField(choices = vote_choices)

    def __str__(self) -> str:
        return f"{self.user} - {'Upvote' if self.vote_type ==1 else 'Downvote'}"
    

class UpvoterAnswer(models.Model):
    vote_choices = ((1,'upvote' ), (-1, 'downvote'))

    answer = models.ForeignKey(Answer, related_name='votes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.SmallIntegerField(choices = vote_choices)

    def __str__(self) -> str:
        return f"{self.user} - {'Upvote' if self.vote_type ==1 else 'Downvote'}"
    

    
    


    