from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Project
from app_games import models


def catalog(request: HttpRequest) -> HttpResponse:
    games = models.GameModel.objects.all()
    
    context = {
        'title': 'Каталог',
        'games': games
    }

    return render(
        request=request,
        template_name='app_games/catalog.html',
        context=context
    )


def game(requst: HttpRequest, author: str, game_title: str) -> HttpResponse:
    context = {
        'title': game_title
    }

    return render(
        request=requst,
        template_name='app_games/details.html',
        context=context
    )