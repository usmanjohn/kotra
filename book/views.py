from typing import Any
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Book, BookCartItem, BookCategory, BookCart, BookOrder, BookRating
from django.views.generic import ListView, DeleteView, DetailView, UpdateView
from .forms import BookForm, ReviewForm

from django.contrib import messages

            
            
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q
from django.views.generic import View

@login_required
def bookcreate(request):

    if request.method == 'POST':
        form = BookForm(request.POST)
    
        if form.is_valid():
            new = form.save(commit=False)
            new.uploader = request.user
            new.save()
            return redirect('/')
    else:
        form = BookForm()
    context = {'form':form}
    return render(request, 'book/book_create.html', context)



def booklist(request):
    books = Book.objects.all()
    
    for book in books:
        if book.prize == None:
            book.prize = 0
        
    context = {'books':books}
    
    return render(request, 'book/book_list.html', context)


def bookdetail(request, pk):
    book = get_object_or_404(Book, id=pk)
    user_reviews = BookRating.objects.filter(book=book).order_by('-date')
    if request.method == 'POST' and request.user.is_authenticated:
        user_review = user_reviews.filter(reviewer=request.user).first()
        
        form = ReviewForm(request.POST, instance=user_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.reviewer = request.user
            review.save()
            messages.success(request, 'Your review has been submitted.')
            return redirect('book-detail', pk=pk)
    else:
        form = ReviewForm()

    is_in_cart = False
    if book.prize == None:
        book.prize = 0
    if request.user.is_authenticated:
        cart = BookCart.objects.filter(user=request.user).first()
        if cart and BookCartItem.objects.filter(cart=cart, book=book).exists():
            is_in_cart = True
    context = {'book': book, 'is_in_cart': is_in_cart, 'user_review':user_reviews, 'form':form}
    return render(request, 'book/book_detail.html', context)

def bookdelete(request, pk):
    book = get_object_or_404(Book, id = pk)
    if request.user.is_authenticated and book.uploader == request.user:
        if request.method == 'POST':
            
            book.delete()
            return redirect('book-list')
    context = {'book':book}
    return render(request, 'book/book_delete.html', context)



def bookupdate(request, pk):
    book = get_object_or_404(Book, id = pk, uploader = request.user)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully')
            return redirect('book-detail', pk = pk)
        else:
            print(form.errors) 
        
    else:
        form = BookForm(instance=book)
    context = {'form':form}
    return render(request, 'book/book_update.html', context)

     
        
        



class AddToCartView(View):
    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        if request.user.is_authenticated:
            cart, created = BookCart.objects.get_or_create(user=request.user)
            cart_item, created = BookCartItem.objects.get_or_create(cart=cart, book=book)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
        return redirect('book-detail', pk=book_id)

class RemoveFromCartView(View):
    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        if request.user.is_authenticated:
            cart = BookCart.objects.filter(user=request.user).first()
            if cart:
                BookCartItem.objects.filter(cart=cart, book=book).delete()
        return redirect('book-detail', pk=book_id)




def see_cart(request):
    if request.user.is_authenticated:
        cart = get_object_or_404(BookCart, user=request.user)
        cart_items = BookCartItem.objects.filter(cart=cart)
        cart_items.total = 0
        
        for cart_item in cart_items:
            try:
                cart_item.prize = cart_item.quantity*cart_item.book.prize
                cart_items.total += cart_item.prize
            except:
                cart_item.prize = 0
        
        return render(request, 'book/book_cart.html', {'cart_items': cart_items})
    else:
        return redirect('login')  # Redirect to login if user is not authenticated

class IncreaseCartItemQuantityView(View):
    def post(self, request, item_id):
        cart_item = get_object_or_404(BookCartItem, id=item_id, cart__user=request.user)
        cart_item.quantity += 1
        
        cart_item.save()
        return redirect('cart-go')

class DecreaseCartItemQuantityView(View):
    def post(self, request, item_id):
        cart_item = get_object_or_404(BookCartItem, id=item_id, cart__user=request.user)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()  # Remove item if quantity is zero
        return redirect('cart-go')

@login_required
def place_order(request):
    products = get_object_or_404(BookCart, user = request.user)
    
    return render(request, 'book/orders.html', context = {'products':products})








