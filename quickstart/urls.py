from django.urls import path
from rest_framework import routers
from . import views
from django.conf.urls import include

app_name = 'quickstart'

urlpatterns = [
    path('detect_signal/', views.detect_situation),
    path('sample/', views.sample),
    path('start/', views.start),
]