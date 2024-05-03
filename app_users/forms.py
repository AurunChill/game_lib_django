from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm


UserModel = get_user_model()

class UserLoginForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = UserModel.objects.filter(email=username).first() or UserModel.objects.filter(username=username).first()
            if user:
                self.user_cache = authenticate(self.request, username=user.username, password=password)
                if self.user_cache is None:
                    raise forms.ValidationError('Неверный пароль.', code='invalid_login')
            else:
                raise forms.ValidationError('Пользователь не найден.', code='invalid_login')

        return self.cleaned_data
