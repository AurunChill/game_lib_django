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
from app_users import views


app_name = 'users'


urlpatterns = [
    path(route='login/', view=views.LoginView.as_view(), name='login'),
    path(route='registration/', view=views.RegistrationView.as_view(), name='registration'),
    path(route='logout/', view=views.LogoutView.as_view(), name='logout'),
    path(route='<str:username>', view=views.UserProfileView.as_view(), name='profile'),
    path(route='change-password/', view=views.UserPasswordChangeView.as_view(), name='password_change'),
]
