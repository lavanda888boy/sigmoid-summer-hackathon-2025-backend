from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.RepoCreateUpdateView.as_view(), name='create-repo'),
    path('search/', views.RepoSearchView.as_view(), name='search-repo'),
    path('filters-list/', views.FiltersListView.as_view(), name='filters-list'),
]
