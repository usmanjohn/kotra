from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.job_list, name = 'job-list'), 
    path('create', views.create_job, name = 'create-job'), 
    path('detail/<pk>', views.job_detail, name = 'job-detail'),
    path('update/<pk>', views.job_update, name = 'job-update'),
    path('delete/<pk>', views.job_delete, name = 'job-delete'),
    path('saved/', views.saved_jobs, name = 'jobs-saved'),
     path('toggle-save/<int:pk>/', views.toggle_save_job, name='job-toggle-save'),
    
]
