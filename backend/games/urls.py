from django.urls import path
from . import views


urlpatterns = [
    path('frontpage/', views.get_frontpage_games, name='frontpage-games'),
    path('company/<int:cid>/', views.get_company, name='get-company-games'),
    path('popular/', views.get_popular_games, name='get-popular'),
    path('mostliked/', views.get_most_like_games, name='get-most-liked-games'),
    path('mostplayed/', views.get_most_play_games, name='get-most-played-games'),
    path('genres/', views.get_genres, name='get-genres'),
    path('<str:slug>/', views.get_game, name='get-game'),
    path('<str:slug>/ratings', views.get_game_ratings, name='get-game-ratings'),
    path('search/<str:name>', views.search_game, name='search-game'),
    path('backdrop/<int:guid>/', views.get_backdrop, name='get-backdrop'),
    path('', views.get_games, name='get-games'),

]
