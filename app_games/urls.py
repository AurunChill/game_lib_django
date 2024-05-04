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
from django.urls import path

# Project
from app_games import views

app_name = 'games'

urlpatterns = [
    path(route='games/', view=views.CatalogView.as_view(), name='catalog'),
    path(route='game/<str:author>/<slug:game_slug>', view=views.GameDetailView.as_view(), name='game_detail') 
]
