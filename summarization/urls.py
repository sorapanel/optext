from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.summaryMain, name='s_main'),
]