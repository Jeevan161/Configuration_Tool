from django.urls import path
from . import views

urlpatterns = [
    path('codingpractice', views.upload_and_prepare, name='upload_and_prepare'),
]
