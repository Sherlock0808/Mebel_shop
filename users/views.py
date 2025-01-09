from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from products.models import Basket, Subcategory
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm, UserEditForm


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('products:index'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'registration1.html', context)


@login_required
def profile(request):
    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            messages.error(request, f'{user_form.errors} & {profile_form.errors}')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
    subcategories = Subcategory.objects.all()
    context = {'title': 'Store - Профиль',
               'user_form': user_form,
               'profile_form': profile_form,
               'subcategories':subcategories
               }
    return render(request, 'profile1.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('products:index'))










