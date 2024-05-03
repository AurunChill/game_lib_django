from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

def login(request: HttpRequest) -> HttpResponse:
    context = {
        'title': 'Вход'
    }

    return render(
        request=request,
        template_name='app_users/auth_login.html',
        context=context
    )


def registration(request: HttpRequest) -> HttpResponse:
    context = {
        'title': 'Регистрация'
    }

    return render(
        request=request,
        template_name='app_users/auth_registration.html',
        context=context
    )