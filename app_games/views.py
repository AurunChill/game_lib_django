from django.views.generic import ListView, DetailView
from django.db.models import F, ExpressionWrapper, DecimalField
from app_games.models import GameModel
from app_games.search import q_search
from django.core.paginator import Paginator

from enum import Enum

class SearchFilters(Enum):
    ALL = 'all'
    DISCOUNT = 'discount'
    FREE = 'free'
    PAID = 'paid'


class CatalogView(ListView):
    model = GameModel
    template_name = 'app_games/catalog.html'
    context_object_name = 'game_list'
    paginate_by = 1

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