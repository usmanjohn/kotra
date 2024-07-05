from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.podcast_list, name='podcast-list'),
    path('detail/<int:pk>/', views.podcast_detail, name='podcast-detail'),
    path('toggle-save/<int:pk>/', views.toggle_save_podcast, name='podcast-toggle-save'),
    path('saved/', views.saved_podcasts, name='podcast-saved'),
]