from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/',  views.LogOut, name = 'logout'), 
    
    path('profiles/list/', views.UsersList.as_view(), name='profile-list'),
    path('profile/<str:username>/', views.view_profile, name='profile'),
    path('profile/<str:username>/update/', views.update_profile, name='profile-update'),
   
    
   
    ]

