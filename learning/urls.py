from django.urls import path
from . import views

urlpatterns = [
    path('skill-tree/', views.skill_tree, name='skill-tree')
]