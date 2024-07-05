from django.forms import ModelForm
from django import forms
from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
          model = Job
          fields = ['title', 'hiring_company',   'position', 'role', 'required_skills', 
                     'required_tools', 'images', 'salary', 'description', 
                    'deadline', 'company_links' ]
          widgets = {
            'deadline': forms.widgets.DateInput(attrs={'type': 'date'})
        }