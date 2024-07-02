from django.contrib import admin

from .models import BookOrder, Book, BookCart, BookCartItem, BookCategory, BookRating
# Register your models here.
admin.site.register([ BookOrder, Book, BookCart, BookCartItem, BookCategory, BookRating])
