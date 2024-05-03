from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator

# Project
from app_games.models import GameModel


def catalog(request: HttpRequest) -> HttpResponse:
    data = request.GET
    page = data.get('page', 1)

    games = GameModel.objects.all()

    paginator = Paginator(object_list=games, per_page=6)
    current_page = int(page)
    current_page_games = paginator.page(current_page)
    
    context = {
        'title': 'Каталог',
        'game_list': current_page_games,
        'current_page': current_page
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