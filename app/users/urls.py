from django.urls import path
from . import views

urlpatterns = [
    path('update-user-prefs/', views.update_user_preferences, name='update-user-preferences'),
]
