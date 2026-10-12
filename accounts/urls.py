from django.urls import path
from . import views as account_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', account_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('profile/edit/', account_views.edit_profile, name='edit-profile'),
    path('profile/<str:username>/', account_views.profile, name='profile')
]
