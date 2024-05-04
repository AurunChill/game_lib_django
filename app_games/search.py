# import django.contrib.postgres.search as search
from django.db.models import Q

# Project
from app_games.models import GameModel


def q_search(query):
    if query.isdigit() and len(query) <= 5:
        return GameModel.objects.filter(id=int(query))

    # Use basic filtering for SQLite as it does not support full-text search as Postgres does
    result = GameModel.objects.filter(
        Q(title__icontains=query) | Q(author__username__icontains=query)
    ).distinct()

    return result


## Full text search for postgres
# def q_search(query):
#     if query.isdigit() and len(query) <= 5:
#         return GameModel.objects.filter(id=int(query))

#     vector = search.SearchVector("name", "description")
#     query = search.SearchQuery(query)

#     result = (
#         GameModel.objects.annotate(rank=search.SearchRank(vector, query))
#         .filter(rank__gt=0)
#         .order_by("-rank")
#     )

#     return result