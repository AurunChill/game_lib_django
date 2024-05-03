from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    context = {
        'title': 'Главная'
    }

    return render(
        request=request, 
        template_name='app_main/index.html',
        context=context
    )


def about(request: HttpRequest) -> HttpResponse:
    context = {
        'title': 'О нас'
    }

    return render(
        request=request, 
        template_name='app_main/about.html',
        context=context
    )


def contacts(request: HttpRequest) -> HttpResponse:
    context = {
        'title': 'Контакты'
    }

    return render(
        request=request, 
        template_name='app_main/contacts.html',
        context=context
    )