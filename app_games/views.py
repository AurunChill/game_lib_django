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