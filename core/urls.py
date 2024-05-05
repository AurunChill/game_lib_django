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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import django.contrib.auth.views as auth_views


password_reset_patterns = [
    path(
        route='password_reset/', 
        view=auth_views.PasswordResetView.as_view(template_name='app_users/password_reset/password_reset_form.html'), 
        name='password_reset'
        ),
    path(
        route='password_reset_done/', 
        view=auth_views.PasswordResetDoneView.as_view(template_name='app_users/password_reset/password_reset_done.html'), 
        name='password_reset_done'
        ),
    path(
        route='password_reset_confirm/<uidb64>/<token>/', 
        view=auth_views.PasswordResetConfirmView.as_view(template_name='app_users/password_reset/password_reset_confirm.html'), 
        name='password_reset_confirm'
        ),
    path(
        route='password_reset_complete/', 
        view=auth_views.PasswordResetCompleteView.as_view(template_name='app_users/password_reset/password_reset_complete.html'), 
        name='password_reset_complete'
        ),
]


urlpatterns = [
    path('', include('app_main.urls')),
    path('admin/', admin.site.urls),
    path('', include('app_games.urls')),
    path('', include('app_carts.urls')),
    path('accounts/', include('app_users.urls')), 
    path('', include(password_reset_patterns)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)