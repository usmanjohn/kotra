from django.contrib import admin

from .models import BookOrder, Book, BookCart, BookCartItem, BookCategory
# Register your models here.
admin.site.register([ BookOrder, Book, BookCart, BookCartItem, BookCategory])
