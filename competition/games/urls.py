from django.urls import path
from . import views

urlpatterns = [
    path('create-team/', views.create_team, name='create_team'),
    path('teams/', views.team_list, name='team_list'),
]
