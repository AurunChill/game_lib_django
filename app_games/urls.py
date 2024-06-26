"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Third-party imports
from django.urls import path

# Project
from app_games import views


app_name = 'games'

api_patterns = [
    path('api/v1/comments/', views.CommentView.as_view(), name='comments'),
    path('api/v1/comments/<int:pk>/', views.CommentView.as_view(), name='comment-detail'),
]

urlpatterns = [
    path(route='games/', view=views.CatalogView.as_view(), name='catalog'),
    path(route='game/<str:author>/<slug:game_slug>/<int:game_id>/', view=views.GameDetailView.as_view(), name='game_detail'),
    path(route='add_to_wishlist/', view=views.WishListItemCreateView.as_view(), name='wishlist_add'),
    path(route='remove_from_wishlist/', view=views.WishListItemRemoveView.as_view(), name='wishlist_remove'),
    path(route='post_game/', view=views.PostGameView.as_view(), name='game_post'),
    path(route='update_game/<slug:game_slug>/<int:game_id>/', view=views.UpdateGameView.as_view(), name='game_update'),
    path(route='delete_game/<slug:game_slug>/<int:game_id>/', view=views.DeleteGameView.as_view(), name='game_delete'),
]


urlpatterns += api_patterns
