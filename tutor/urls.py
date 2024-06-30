from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from django.views.generic import RedirectView





urlpatterns = [
    
    path('list', views.tutors_list, name = 'tutors-list'), 
    path('tags/<slug:tag_slug>/', views.tag_list, name = 'tutors-tags'), 
    path('detail/<pk>', views.tutors_detail, name = 'tutor-detail'),
    
    path('create', views.tutors_create, name = 'tutor-create'),
    path('update/<pk>', views.tutor_update, name = 'tutor-update'),
    path('delete/<pk>', views.tutor_delete, name = 'tutor-delete'),
    
    
]