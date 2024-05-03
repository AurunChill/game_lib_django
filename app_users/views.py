from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
import django.contrib.auth as auth
from django.contrib.auth.decorators import login_required

# Project
from app_users.forms import UserLoginForm, UserRegistrationForm


def login(request: HttpRequest) -> HttpResponse:
    data = request.POST
    if data:
        form = UserLoginForm(data=data)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return redirect(user.get_absolute_url())  # Redirect user to home page or another appropriate page
    else:
        form = UserLoginForm()

    context = {
        'title': 'Вход',
        'form': form,
    }

    return render(
        request=request,
        template_name='app_users/auth_login.html',
        context=context
    )


def registration(request: HttpRequest) -> HttpResponse:
    data = request.POST
    if data:
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('games:catalog'))  # Redirect to a different page after successful registration
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'Регистрация',
        'form': form
    }

    return render(
        request=request,
        template_name='app_users/auth_registration.html',
        context=context
    )


@login_required
def logout(request: HttpRequest) -> HttpResponse:
    auth.logout(request=request)

    return redirect(reverse('users:login'))


@login_required()
def user_profile(request: HttpRequest, username: str) -> HttpResponse:
    context = {
        'title': username
    }

    return render(
        request=request,
        template_name='app_users/profile.html',
        context=context
    )
