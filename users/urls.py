from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/',  views.LogOut, name = 'logout'), 
    
    path('profiles/list/', views.UsersList.as_view(), name='profile-list'),
    path('profile/<str:username>/', views.view_profile, name='profile'),
    path('profile/<str:username>/update/', views.update_profile, name='profile-update'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('profile/update/email/', views.update_email, name='update_email'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    
    path('profile/update/password/', auth_views.PasswordChangeView.as_view(template_name='users/password_change.html'), name='password_change'),
    path('profile/update/password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),
]
    
   


