from django.urls import path
from . import views

app_name = 'inquiries'

urlpatterns = [
    path('submit-inquiry/', views.submit_inquiry, name='submit_inquiry'),
]
