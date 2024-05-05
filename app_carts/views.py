from django.http import JsonResponse
from django.views.generic import ListView
from django.views import View
    
# Standard
from decimal import Decimal
import json

 # Project
from app_carts.models import CartItemModel
from app_games.models import GameModel
from app_users.models import UserModel


class CartViewList(ListView):
    model = CartItemModel
    template_name = 'app_carts/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self): 
        queryset = super().get_queryset() 

        current_user = self.request.user
        queryset = queryset.filter(user__username=current_user.username)

        return queryset

    def get_context_data(self, **kwargs):
        items = self.get_queryset()
        games_price = sum(item.game.total_price() for item in items)
        percent_price = games_price * Decimal(0.01)
        total_price = games_price + percent_price

        context = super().get_context_data(**kwargs)
        context['title'] = 'Корзина'
        context['games_price'] = games_price
        context['percent_price'] = percent_price
        context['total_price'] = total_price
        context['cart_items'] = self.get_queryset()
        return context


class CartItemCreateView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            game_id = data.get('game_id')
            user_id = data.get('user_id')
            if game_id and user_id:
                game = GameModel.objects.get(pk=game_id)
                user = UserModel.objects.get(pk=user_id)
                if game and user:
                    CartItemModel.objects.create(user=user, game=game)
                    return JsonResponse({'message': 'Cart item created successfully'})
                else:
                    return JsonResponse({'error': 'No such game or user in database'}, status=400)
            else:
                 return JsonResponse({'error': 'game_id or user_id is missing'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)


class CartItemRemoveView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            game_id = data.get('game_id')
            user_id = data.get('user_id')
            if game_id and user_id:
                game = GameModel.objects.get(pk=game_id)
                user = UserModel.objects.get(pk=user_id)
                if game and user:
                    CartItemModel.objects.filter(user=user).filter(game=game).delete()
                    return JsonResponse({'message': 'Cart item deleted successfully'})
                else:
                    return JsonResponse({'error': 'No such game or user in database'}, status=400)
            else:
                 return JsonResponse({'error': 'game_id or user_id is missing'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)