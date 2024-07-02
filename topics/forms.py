from django.forms import ModelForm
from django import forms
from .models import Topic,Answer, Upvoter, UpvoterAnswer


from django_ckeditor_5.widgets import CKEditor5Widget

class TopicForm(forms.ModelForm):
      """Form for comments to the article."""
       
      topic_body = forms.CharField(widget=CKEditor5Widget(config_name='extends'))

      class Meta:
          model = Topic
          fields = ['topic_category', 'topic_title', 'topic_body',  'hashtag']
          

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_body']


class UpwoteForm(ModelForm):
    class Meta:
        model = Upvoter
        fields = ['vote_type']

class AnswerUpwoteForm(ModelForm):
    class Meta:
        model = UpvoterAnswer
        fields = ['vote_type']
        