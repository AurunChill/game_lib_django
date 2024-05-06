from typing import Any
from django import forms

# Project
from app_games.models import GameModel


class BaseGameForm(forms.ModelForm):
    image = forms.ImageField(required=True)
    title = forms.CharField(required=True, max_length=150)
    description = forms.CharField(required=False, widget=forms.TextInput())
    release_date = forms.DateTimeField(required=True, widget=forms.DateTimeInput())
    price = forms.DecimalField(required=True, min_value=0)
    discount = forms.IntegerField(required=False, min_value=0, max_value=100)

    class Meta:
        model = GameModel
        fields = ['image', 'title', 'description', 'release_date', 'price', 'discount'] 


class GameCreateForm(BaseGameForm):
    pass

class GameUpdateForm(BaseGameForm):
    pass