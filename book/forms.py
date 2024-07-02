from .models import Book, BookCart,BookCartItem,BookCategory,BookOrder, BookRating
from django.forms import ModelForm
from django import forms

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'author', 'num_of_pages', 'pub_year','category', 'cover_image', 'prize']



class ReviewForm(ModelForm):
    class Meta:
        model = BookRating
        fields = ['rating', 'review']
        widgets = {
            'review': forms.Textarea(attrs={'rows': 4}),
        }
      