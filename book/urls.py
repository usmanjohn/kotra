from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views




urlpatterns = [
    path('list/', views.booklist, name = 'book-list'),
    path('create/', views.bookcreate, name = 'book-create'),
    path('detail/<pk>', views.bookdetail, name = 'book-detail'),
    path('add-to-cart/<int:book_id>/', views.AddToCartView.as_view(), name='add-to-cart'),
    path('remove-from-cart/<int:book_id>/', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('see-cart/', views.see_cart, name='cart-go'),
    path('increase-quantity/<int:item_id>/', views.IncreaseCartItemQuantityView.as_view(), name='increase-quantity'),
    path('decrease-quantity/<int:item_id>/', views.DecreaseCartItemQuantityView.as_view(), name='decrease-quantity'),
    path('order/', views.place_order, name = 'order'),
    path('delete/<pk>', views.bookdelete, name = 'book-delete'),
    path('update/<pk>', views.bookupdate, name = 'book-update')
]
