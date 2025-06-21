from django.urls import path
from . import views

urlpatterns = [
    path('callback/', views.github_oauth_callback, name='github-oauth-callback'),
]
