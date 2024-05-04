from typing import Any
from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm,
    PasswordChangeForm
)

UserModel = get_user_model()

class UserLoginForm(AuthenticationForm):
    def clean(self) -> dict[str, Any]:
        super().clean()
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


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password1', 'password2')

    def clean(self) -> dict[str, Any]:
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1')
        password_repeated = self.cleaned_data.get('password2')
        if username and email and password and password and password_repeated:
            user_by_username = UserModel.objects.filter(username=username).first()
            user_by_email = UserModel.objects.filter(email=email).first()
            if not user_by_username and not user_by_email:
                if password != password_repeated:
                    raise forms.ValidationError('Пароли не совпадают', code='invalid_registration')
            else:
                raise forms.ValidationError('Аккаунт с таким именем/почтой уже существует', code='invalid_registration')

        return self.cleaned_data 
    

class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordChangeForm, self).__init__(*args, **kwargs)
        
        self.fields['old_password'].widget.attrs['id'] = 'old_password'
        self.fields['new_password1'].widget.attrs['id'] = 'new_password1'
        self.fields['new_password2'].widget.attrs['id'] = 'new_password2'

