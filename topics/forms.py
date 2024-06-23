from django.forms import ModelForm
from django import forms
from .models import Topic,Answer, Upvoter, UpvoterAnswer


from django_ckeditor_5.widgets import CKEditor5Widget

class TopicForm(forms.ModelForm):
      """Form for comments to the article."""

      def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields["topic_body"].required = False

      class Meta:
          model = Topic
          fields = ['topic_category', 'topic_title', 'topic_body', 'topic_hashtag', 'hashtag']
          widgets = {
              "text": CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="comment"
              )
          }


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
        