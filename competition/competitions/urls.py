from django.urls import path
from . import views


urlpatterns = [
    path('<int:tournament_id>/leaderboard/',
         views.tournament_leaderboard,name='tournament_leaderboard'),
]