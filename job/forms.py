from django.forms import ModelForm
from django import forms
from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
          model = Job
          fields = ['title', 'hiring_company',  'description', 'position', 'qualifications', 'required_skills', 
                     'required_tools', 'images', 'salary',  
                    'deadline', 'company_links' ]
          widgets = {
            'deadline': forms.widgets.DateInput(attrs={'type': 'date'})
        }