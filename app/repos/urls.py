from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_repo, name='create-repo'),
    path('search/', views.RepoSearchView.as_view(), name='search-repo'),
]
