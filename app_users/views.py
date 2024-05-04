import django.contrib.auth as auth
from django.urls import reverse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView

# Project
from app_users.forms import UserLoginForm, UserRegistrationForm, UserPasswordChangeForm


class LoginView(FormView):
    form_class = UserLoginForm
    template_name = 'app_users/auth_login.html'
    success_url = reverse_lazy('games:catalog') # You need to define the URL to redirect after login

    def form_valid(self, form):
        user = form.get_user()
        auth.login(self.request, user)
        return super().form_valid(form) 


class RegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'app_users/auth_registration.html'
    success_url = reverse_lazy('users:login')  # Adjust to the correct URL based on your URL configuration

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class LogoutView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        auth.logout(request)
        return redirect(reverse('users:login'))


class UserProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'app_users/profile.html'
    context_object_name = 'profile'
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.username
        return context
    

class UserPasswordChangeView(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'app_users/password_change.html'

    def get_success_url(self):
        return self.request.user.get_absolute_url()