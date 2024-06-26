
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


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

class UserProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ['image', 'bio', 'instagram_url', 'facebook_url', 'twitter_url', 'youtube_url', 'other_url', 'link_image']

        