from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field 
class Test(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

    
class Question(models.Model):
    QUESTION_TYPES = (
        ('MC', 'Multiple Choice'),
        ('WA', 'Written Answer'),
    )
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question_text=CKEditor5Field('Question', config_name='extends')
    
    question_type = models.CharField(max_length=2, choices=QUESTION_TYPES)
    def __str__(self):
        return self.question_text[:20]


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)


class TestAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(default=0)

    def calculate_score(self):
        total_questions = self.test.question_set.count()
        correct_answers = self.useranswer_set.filter(is_correct=True).count()
        self.score = (correct_answers / total_questions) * 100
        self.save()

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True)
    written_answer = models.TextField(null=True, blank=True)
    test_instance = models.ForeignKey(Test, on_delete=models.CASCADE, null=True)
    test_attempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE, null = True)
    is_correct = models.BooleanField(default=False)
