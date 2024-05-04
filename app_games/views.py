from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import F, ExpressionWrapper, DecimalField

# Standard
from enum import Enum

# Project
from app_games.models import GameModel


class SearchFilters(Enum):
    ALL = 'all'
    DISCOUNT = 'discount'
    FREE = 'free'
    PAID = 'paid'


def catalog(request: HttpRequest) -> HttpResponse:
    games = GameModel.objects.all()
    data = request.GET
    if data:
        search_filter = data.get('pricing_type', SearchFilters.ALL.value).lower()
        match search_filter:
            case SearchFilters.DISCOUNT.value:
                games = GameModel.objects.filter(discount__gt=0)
            case SearchFilters.PAID.value:
                games = GameModel.objects.filter(discount=0)
            case SearchFilters.FREE.value:
                games = GameModel.objects.annotate(
                    total_price=ExpressionWrapper(
                        F('price') * (1 - F('discount') / 100),
                        output_field=DecimalField(),
                    )
                ).filter(total_price=0)
                
    page = data.get('page', 1)

    paginator = Paginator(object_list=games, per_page=6)
    current_page = int(page)
    current_page_games = paginator.page(current_page)

    context = {
        'title': 'Каталог',
        'game_list': current_page_games,
        'current_page': current_page,
    }

    return render(
        request=request, template_name='app_games/catalog.html', context=context
    )


def game(requst: HttpRequest, author: str, game_slug: str) -> HttpResponse:
    game = (
        GameModel.objects.filter(author__username=author).filter(slug=game_slug).first()
    )

    context = {'title': game.title, 'game': game}

    return render(
        request=requst, template_name='app_games/details.html', context=context
    )
