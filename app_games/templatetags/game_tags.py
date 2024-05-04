from django import template
from django.utils.http import urlencode

# Project
from app_games.models import GameModel, WishListModel
from app_users.models import UserModel
from app_carts.models import CartItemModel


register = template.Library()


@register.simple_tag(takes_context=True)
def set_query_params(context, **kwargs):
    query = context.get('request').GET.dict()
    query.update(kwargs)
    return urlencode(query)


@register.simple_tag()
def in_user_cart(user_id: int, game_id: int):
    game = GameModel.objects.get(pk=game_id)
    user = UserModel.objects.get(pk=user_id)

    if game and user:
        return CartItemModel.objects.filter(user=user, game=game).exists()
    return False
    

@register.simple_tag()
def in_user_wishlist(user_id: int, game_id: int):
    game = GameModel.objects.get(pk=game_id)
    user = UserModel.objects.get(pk=user_id)

    if game and user:
        return WishListModel.objects.filter(user=user, game=game).exists()
    return False