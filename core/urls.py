from django.urls import path
from .views import HomePage, LandingPage, Resources

urlpatterns = [
    path('home/', HomePage.as_view(), name='home'),
    path('', LandingPage.as_view(), name='landing-page'),
    path('resources/', Resources.as_view(), name='resources')
]