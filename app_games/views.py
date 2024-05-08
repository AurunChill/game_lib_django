from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views import View
from django.db.models import F, ExpressionWrapper, DecimalField
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Standard
from enum import Enum
import json

# Project
from app_games.models import GameModel, WishListModel
from app_games.search import q_search
from app_games.forms import GameCreateForm, GameUpdateForm
from app_users.models import UserModel


class SearchFilters(Enum):
    ALL = 'all'
    DISCOUNT = 'discount'
    FREE = 'free'
    PAID = 'paid'
    WISHLISTED = 'wishlisted'
    MINE = 'mine'


class OrderFilters(Enum):
    NEW = 'new'
    OLD = 'old'
    POPULAR = 'popular'


class CatalogView(ListView):
    """
    Display a catalog of games with optional filters and search.
    """
    model = GameModel
    template_name = 'app_games/catalog.html'
    context_object_name = 'game_list'

    def get_queryset(self):
        """
        Retrieve the queryset based on search and filter criteria.
        """
        queryset = super().get_queryset()
        queryset = self.apply_search(queryset)
        queryset = self.apply_filters(queryset)
        queryset = self.apply_order(queryset)
        return self.paginate_queryset(queryset)

    def apply_search(self, queryset):
        """
        Apply search query to the queryset if search parameter is provided.
        """
        query = self.request.GET.get('search')
        return q_search(query) if query else queryset
    
    def apply_order(self, queryset):
        """
        Apply order query to the queryset if order parameter is provided.
        """
        order_filter = self.request.GET.get('order', OrderFilters.NEW.value).lower()
        match order_filter:
            case OrderFilters.NEW.value:
                return queryset.order_by('-release_date')
            case OrderFilters.OLD.value:
                return queryset.order_by('release_date')
            case OrderFilters.POPULAR.value:
                return queryset.annotate(wishlist_count=Count('wishlist_game')).order_by('-wishlist_count')
            case _:
                return queryset


    def apply_filters(self, queryset):
        """
        Apply filter based on the pricing_type parameter to the queryset.
        """
        search_filter = self.request.GET.get('pricing_type', SearchFilters.ALL.value).lower()
        match search_filter:
            case SearchFilters.DISCOUNT.value:
                return queryset.filter(discount__gt=0)
            case SearchFilters.PAID.value:
                return queryset.filter(price__gt=0)
            case SearchFilters.FREE.value:
                return self.filter_free_games(queryset)
            case SearchFilters.WISHLISTED.value:
                return self.filter_wishlisted_games(queryset)
            case SearchFilters.MINE.value:
                return self.filter_owned_games(queryset)
            case _:
                return queryset

    def filter_free_games(self, queryset):
        """
        Filter queryset to include only games that are effectively free.
        """
        return queryset.annotate(
            total_price=ExpressionWrapper(
                F('price') * (1 - F('discount') / 100),
                output_field=DecimalField(),
            )
        ).filter(total_price=0)

    def filter_wishlisted_games(self, queryset):
        """
        Filter queryset to include only games that are wishlisted by the current user.
        """
        user = self.request.user
        if user.is_authenticated:
            wishlist_games = WishListModel.objects.filter(user=user).values_list('game', flat=True)
            return queryset.filter(pk__in=wishlist_games)
        return GameModel.objects.none()

    def filter_owned_games(self, queryset):
        """
        Filter queryset to include only games owned by the current user.
        """
        user = self.request.user
        if user.is_authenticated:
            return queryset.filter(author=user)
        return GameModel.objects.none()

    def paginate_queryset(self, queryset):
        """
        Paginate the queryset.
        """
        page = self.request.GET.get('page', 1)
        paginator = Paginator(queryset, per_page=6)
        return paginator.get_page(page)

    def get_context_data(self, **kwargs):
        """
        Get the context for this view.
        """
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

    def get_object(self, queryset=None):
        author = self.kwargs.get('author')
        game_slug = self.kwargs.get('game_slug')
        game_id = self.kwargs.get('game_id')
        
        if queryset is None:
            queryset = self.get_queryset()
        
        game = get_object_or_404(queryset, author__username=author, slug=game_slug, id=game_id)
        return game

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_wishlists_count = len(WishListModel.objects.filter(game=self.object))

        context['title'] = self.object.title
        context['total_wishlists_count'] = total_wishlists_count
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
        

class PostGameView(LoginRequiredMixin, CreateView ):
    model = GameModel
    form_class = GameCreateForm
    template_name = 'app_games/post_game.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        self.success_url = reverse_lazy(self.object.get_absolute_url())  
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Post a Game'
        if self.request.method == 'POST':
            context['form'] = GameCreateForm(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['form'] = GameCreateForm(instance=self.object)
        return context 
    

class UpdateGameView(LoginRequiredMixin, UpdateView):
    model = GameModel
    form_class = GameUpdateForm
    template_name = 'app_games/update_game.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        self.success_url = reverse_lazy(self.object.get_absolute_url())  
        return response

    def get_object(self):
        author = self.request.user
        game_id = self.kwargs.get('game_id')
        game_slug = self.kwargs.get('game_slug')
        game = GameModel.objects.filter(author=author).filter(slug=game_slug).filter(id=game_id).first()
        return game

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update a Game'
        if self.request.method == 'POST':
            context['form'] = GameUpdateForm(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['form'] = GameUpdateForm(instance=self.object)
        game = self.get_object()
        context['game'] = game
        return context 


class DeleteGameView(LoginRequiredMixin, DeleteView):
    model = GameModel
    success_url = reverse_lazy('games:catalog')

    def get_object(self):
        author = self.request.user
        game_id = self.kwargs.get('game_id')
        game_slug = self.kwargs.get('game_slug')
        game = GameModel.objects.filter(author=author).filter(slug=game_slug).filter(id=game_id).first()
        return game

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Game'
        game = self.get_object()
        context['game'] = game
        return context

    def delete(self):
        self.object = self.get_object()
        self.object.delete()
        messages.add_message(self.request, messages.INFO, 'Игра успешно удалена!')
        return self.success_url