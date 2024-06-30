from django.forms import ModelForm
from django import forms
from .models import Tutoring
from django_ckeditor_5.widgets import CKEditor5Widget
class TutoringForm(forms.ModelForm):
      """Form for comments to the article."""

       

      class Meta:
          model = Tutoring
          fields = ['title', 'description', 'tags', 'category', 'short_description']
          


      