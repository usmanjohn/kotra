
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class EmailChangeForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EmailChangeForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError('This email is already in use.')
        return email

class ProfileUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image', 'bio', 'instagram_url', 'facebook_url', 'twitter_url', 'youtube_url', 'other_url', 'link_image']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    user_image = forms.ImageField(required=False)
    class Meta:
        model = User
        fields = ['username', 'email', 'user_image' ]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields =['username', 'email']

        