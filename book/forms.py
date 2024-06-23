from .models import Book, BookCart,BookCartItem,BookCategory,BookOrder
from django.forms import ModelForm

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'author', 'num_of_pages', 'pub_year','category', 'cover_image', 'prize']