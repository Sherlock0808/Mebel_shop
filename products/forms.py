from django import forms
from .models import Messages

class MessageForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'contact__section-input', 'placeholder': 'Имя'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'contact__section-input', 'placeholder': 'Введите адрес эл. почты'
    }))
    message = forms.CharField(widget=forms.TextInput(attrs={
        'name': 'message', 'class': 'contact__section-message'
    }))

    class Meta:
        model = Messages
        fields = ('name', 'email', 'message')
