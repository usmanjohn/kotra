from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    title = models.CharField(max_length=40)
    hiring_company = models.CharField(max_length = 70)
    uploader = models.ForeignKey(User, related_name = 'jobs', on_delete=models.SET_NULL, null=True)
    position = models.CharField(max_length=50)

    required_skills = models.TextField(null=True, blank = True)
    required_tools = models.TextField(null = True, blank = True)

    images = models.ImageField(upload_to='jobs', default='jobs/default.png')

    role = models.TextField(blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)


    description = models.TextField()
    
    date_posted = models.DateField(auto_now_add=True)
    deadline = models.DateField(blank=True, null=True)

    company_links = models.URLField(blank=True, null=True)



