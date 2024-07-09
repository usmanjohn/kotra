from typing import Any
from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    title = models.CharField(max_length=40)
    hiring_company = models.CharField(max_length = 70)
    uploader = models.ForeignKey(User, related_name = 'jobs', on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    position = models.CharField(max_length=50)
    required_skills = models.TextField(null=True, blank = True)
    required_tools = models.TextField(null = True, blank = True)
    images = models.ImageField(upload_to='jobs', default='jobs/default.png')
    qualifications = models.TextField(blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    date_posted = models.DateField(auto_now_add=True)
    deadline = models.DateField(blank=True, null=True)
    company_links = models.URLField(blank=True, null=True) 

    def __str__(self):
        return self.title


class SavedJobs(models.Model):  # Changed class name to follow Python naming conventions
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_job')
    date_saved = models.DateTimeField(auto_now_add=True)  # Changed to use timezone.now without parentheses

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"    

