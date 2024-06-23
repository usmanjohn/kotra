
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('list/', views.podcast_list, name = 'podcast-list'),
    path('detail/<pk>', views.podcast_detail, name = 'podcast-detail'),
    path('save/<pk>', views.save_podcast, name = 'podcast-save'),
    path('unsave/<pk>', views.unsave_podcast, name = 'podcast-unsave'),
    path('saved/', views.saved_podcasts, name = 'podcast-saved'),
    
]