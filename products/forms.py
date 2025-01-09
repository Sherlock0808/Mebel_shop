from django import forms
from .models import Messages


class MessageForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'contact__section-input', 'placeholder': 'Имя'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'contact__section-input', 'placeholder': 'email'
    }))
    messages = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'contact__section-input', 'placeholder': 'текст'
    }))

    class Meta:
        model = Messages
        fields = ('name', 'email', 'messages')


class PaymentForm(forms.Form):
    name = forms.CharField(max_length=100, label="Имя", widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": "form-control"}))