"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path, register_converter

# Project
from app_games import views
from app_games import converters

register_converter(converter=converters.FourDigitYearConverter, type_name='year')

urlpatterns = [
    path(route='', view=views.index, name='home'),
    path(route='cats/<int:cat_id>/', view=views.categories, name='cats_id'),
    path(route='cats/<slug:cat_slug>/', view=views.categories_by_slug, name='cats_slug'),
    path(route='archive/<year:year>/', view=views.archive, name='archive')
    # re_path(route=r'^archive/(?P<year>[0-9]{4})/', view=views.archive)
]
