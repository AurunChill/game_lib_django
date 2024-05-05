import django.contrib.auth as auth
from django.urls import reverse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView

# Project
import app_users.forms as forms


class LoginView(FormView):
    form_class = forms.UserLoginForm
    template_name = 'app_users/auth_login.html'
    success_url = reverse_lazy('games:catalog') # You need to define the URL to redirect after login

    def form_valid(self, form):
        user = form.get_user()
        messages.add_message(self.request, messages.INFO, 'Вы вошли в аккаунт!')

        auth.login(self.request, user)
        return super().form_valid(form) 


class RegistrationView(CreateView):
    form_class = forms.UserRegistrationForm
    template_name = 'app_users/auth_registration.html'
    success_url = reverse_lazy('users:login')  # Adjust to the correct URL based on your URL configuration

    def form_valid(self, form):
        self.object = form.save()
        messages.add_message(self.request, messages.INFO, 'Вы успешно зарегестрировались! Теперь войдите в аккаунт')

        return super().form_valid(form)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
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
        if self.request.method == 'POST':
            context['form'] = forms.UserInfoUpdateForm(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['form'] = forms.UserInfoUpdateForm(instance=self.object)
        return context 

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = forms.UserInfoUpdateForm(request.POST, request.FILES, instance=self.object)
        if form.is_valid():
            form.save()
            return redirect(self.get_success_url())
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return self.object.get_absolute_url()


class UserPasswordChangeView(PasswordChangeView):
    form_class = forms.UserPasswordChangeForm
    template_name = 'app_users/password_change.html'

    def get_success_url(self):
        return self.request.user.get_absolute_url()