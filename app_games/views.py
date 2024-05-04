from django.views.generic import ListView, DetailView
from django.views import View
from django.db.models import F, ExpressionWrapper, DecimalField
from django.http import JsonResponse
from django.core.paginator import Paginator

# Project
from app_games.models import GameModel, WishListModel
from app_games.search import q_search
from app_users.models import UserModel

# Standard
from enum import Enum
import json


class SearchFilters(Enum):
    ALL = 'all'
    DISCOUNT = 'discount'
    FREE = 'free'
    PAID = 'paid'
    WISHLISTED = 'wishlisted'


class CatalogView(ListView):
    model = GameModel
    template_name = 'app_games/catalog.html'
    context_object_name = 'game_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('search')
        if query:
            queryset = q_search(query)
        search_filter = self.request.GET.get('pricing_type', SearchFilters.ALL.value).lower()
        match search_filter:
            case SearchFilters.DISCOUNT.value:
                queryset = queryset.filter(discount__gt=0)
            case SearchFilters.PAID.value:
                queryset = queryset.filter(price__gt=0)
            case SearchFilters.FREE.value:
                queryset = queryset.annotate(
                    total_price=ExpressionWrapper(
                        F('price') * (1 - F('discount') / 100),
                        output_field=DecimalField(),
                    )
                ).filter(total_price=0)
            case SearchFilters.WISHLISTED.value:
                user = self.request.user  # Get the current user
                if user.is_authenticated:
                    wishlist_games = WishListModel.objects.filter(user=user).values_list('game')
                    queryset = queryset.filter(pk__in=wishlist_games)
                else:
                    queryset = GameModel.objects.none()
                
        page = int(self.request.GET.get('page', 1))
        paginator = Paginator(object_list=queryset, per_page=6)
        return paginator.get_page(page)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Каталог'
        context['current_page'] = int(self.request.GET.get('page', 1))
        context['game_list'] = self.get_queryset()
        return context


class GameDetailView(DetailView):
    model = GameModel
    template_name = 'app_games/details.html'
    context_object_name = 'game'
    slug_url_kwarg = 'game_slug'
    slug_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(author__username=self.kwargs.get('author'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context
    

class WishListItemCreateView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            game_id = data.get('game_id')
            user_id = data.get('user_id')
            if game_id and user_id:
                game = GameModel.objects.get(pk=game_id)
                user = UserModel.objects.get(pk=user_id)
                if game and user:
                    WishListModel.objects.create(user=user, game=game)
                    return JsonResponse({'message': 'WishList item created successfully'})
                else:
                    return JsonResponse({'error': 'No such game or user in database'}, status=400)
            else:
                 return JsonResponse({'error': 'game_id or user_id is missing'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)


class WishListItemRemoveView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            game_id = data.get('game_id')
            user_id = data.get('user_id')
            if game_id and user_id:
                game = GameModel.objects.get(pk=game_id)
                user = UserModel.objects.get(pk=user_id)
                if game and user:
                    WishListModel.objects.filter(user=user).filter(game=game).delete()
                    return JsonResponse({'message': 'WishList item deleted successfully'})
                else:
                    return JsonResponse({'error': 'No such game or user in database'}, status=400)
            else:
                 return JsonResponse({'error': 'game_id or user_id is missing'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)