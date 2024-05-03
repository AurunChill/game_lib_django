from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Project
from app_games.models import GameModel


def catalog(request: HttpRequest) -> HttpResponse:
    games = GameModel.objects.all()
    
    context = {
        'title': 'Каталог',
        'game_list': games
    }

    return render(
        request=request,
        template_name='app_games/catalog.html',
        context=context
    )


def game(requst: HttpRequest, author: str, game_slug: str) -> HttpResponse:
    game = GameModel.objects.filter(author__username=author).filter(slug=game_slug).first()

    context = {
        'title': game.title,
        'game': game
    }

    return render(
        request=requst,
        template_name='app_games/details.html',
        context=context
    )