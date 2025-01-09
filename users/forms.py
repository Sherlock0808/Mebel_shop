from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from users.models import User, Profile


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'contact__section-input', 'placeholder': 'Введите ваш юзернейм'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'contact__section-input', 'placeholder': 'Введите ваш пароль'
    }))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'contact__section-input', 'placeholder': 'Создайте username'
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'contact__section-input', 'placeholder': 'Введите ваше имя'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'contact__section-input', 'placeholder': 'Введите вашу фамилию'
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'contact__section-input', 'placeholder': 'Введите номер телефона'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'contact__section-input', 'placeholder': 'Введите ваш email'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'contact__section-input', 'placeholder': 'Введите ваш пароль'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'contact__section-input', 'placeholder': 'Подтвердите ваш пароль'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone_number', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'contact__section-input'}))
    street = forms.CharField(widget=forms.TextInput(attrs={'class': 'contact__section-input'}))
    suite = forms.CharField(widget=forms.TextInput(attrs={'class': 'contact__section-input'}))
    apartment = forms.CharField(widget=forms.TextInput(attrs={'class': 'contact__section-input'}))

    class Meta:
        model = Profile
        fields = ('city', 'street', 'suite', 'apartment')


class UserEditForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'contact__section-input'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'contact__section-input'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'contact__section-input'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'contact__section-input'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'contact__section-input'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'phone_number')