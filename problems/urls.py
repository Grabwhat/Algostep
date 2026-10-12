from django.urls import path
from .views import ProblemDetailView
from . import views

urlpatterns = [
    path('problem-detail/<slug:slug>/', ProblemDetailView.as_view(), name='problem-detail'),
    path('problem-list/<slug:topic>/', views.problem_list, name='problem-list')
]