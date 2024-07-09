from django.db import models
from django.contrib.auth.models import User
import datetime
import random
from django.utils import timezone
from django.db.models import Avg

Rating = (
    (1, '★☆☆☆☆'),
    (2, '★★☆☆☆'),
    (3, '★★★☆☆'),
    (4, '★★★★☆'),
    (5, '★★★★★')
    
)
class BookCategory(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    YEAR_CHOICES = []
    for r in range(1980, (datetime.datetime.now().year+1)):
        YEAR_CHOICES.append((r,r))

    
    title = models.CharField(max_length=40)
    uploader = models.ForeignKey(User, related_name='books_uploaded',on_delete=models.CASCADE)
    description = models.TextField()
    num_of_pages = models.IntegerField()
    cover_image = models.ImageField(upload_to='book_covers', default='book_covers/default.png')
    author = models.CharField(max_length=50)
    pub_year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    category = models.ForeignKey(BookCategory, on_delete=models.CASCADE, null=True, blank=True)
    prize = models.FloatField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    @property
    def avg_rating(self):
        rating = self.review.aggregate(models.Avg('rating'))['rating__avg']
        if rating is not None:
            rounded_rating = round(rating)
            return dict(Rating).get(rounded_rating, '☆☆☆☆☆')
        return '☆☆☆☆☆'
class BookCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart of {self.user.username}"

class BookCartItem(models.Model):
    cart = models.ForeignKey(BookCart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.book.title} in cart of {self.cart.user.username}"

class BookOrder(models.Model):
    cart = models.ForeignKey(BookCart, on_delete=models.CASCADE) 
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Use DecimalField for monetary values
    date = models.DateField(auto_now_add=True) 

    def __str__(self):
        return f"Order #{self.id} - {self.cart.user.username}"
    
class BookRating(models.Model):
    reviewer = models.ForeignKey(User, related_name='book_review', on_delete= models.CASCADE)
    book = models.ForeignKey(Book, related_name = 'review', on_delete=models.CASCADE)
    review = models.TextField(blank = True, null=True)
    rating = models.IntegerField(choices=Rating, default=None)
    date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.book.title
    def get_rating(self): 
        return self.rating 
   
