from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_list, name='test_list'),
    path('test/<int:test_id>/', views.take_test, name='take_test'),
    path('test/<int:test_id>/submit/', views.submit_test, name='submit_test'),
    path('test/<int:test_id>/results/<int:attempt_id>/', views.test_results, name='test_results'),
]
