from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
import datetime
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.
class Tutoring(models.Model):
    status_choice = (('submitted', 'submitted'), ('in_review', 'in_review'), ('posted', 'posted'))
    category_choice = (('topik', 'Topik'), ('daily', 'Daily'), ('kiip', 'KIIP'), ('visa', 'Visa'), ('other', 'other'))
    title = models.CharField(max_length=40)
    description=CKEditor5Field('Description', config_name='extends')
    short_description = models.CharField('Describe shortly what it is about',max_length=200, default='No short describtion provided, you can read full description')
    author = models.ForeignKey(User, related_name = 'tutoring', on_delete=models.SET_NULL, null=True)
    status = models.CharField(choices=status_choice, default='submitted', max_length=20)
    category = models.CharField(choices= category_choice, default='topik', max_length=20)
    date = models.DateField(auto_now_add=True)    
    tags = TaggableManager(blank=True)

    

    
    
    
