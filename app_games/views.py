from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse


def categories(request: HttpRequest, cat_id: int = 0) -> HttpResponse:
    return HttpResponse(f'Categories {cat_id}')


def categories_by_slug(request: HttpRequest, cat_slug: str) -> HttpResponse:
    print(request.GET)
    return HttpResponse(f'Categories {cat_slug}')


def archive(request: HttpRequest, year: int) -> HttpResponse:
    if year > 2024:
        # raise Http404()
        return redirect(reverse('cats_slug', args=('test_slug', ))) # permanent=True for 301 error
    return HttpResponse(f'Categories archive by {year}')


def page_not_found(request, exception) -> HttpResponseNotFound:
    return HttpResponseNotFound('<h1>Страница не найдена!</h1>')