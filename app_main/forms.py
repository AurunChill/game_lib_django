from typing import Any
from django import forms


class SendMessageForm(forms.Form):
    name = forms.CharField()
    contact_email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    