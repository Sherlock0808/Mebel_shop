from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from users.forms import UserLoginForm, UserRegistrationForm, UserEditForm, UserProfileForm
from products.models import Basket, Subcategory


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(email=email, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('products:index'))
    else:
        form = UserLoginForm()
    subcategories = Subcategory.objects.all()
    sub_1 = subcategories[0:4]
    sub_2 = subcategories[4:7]
    sub_3 = subcategories[6]
    context = {'form': form,
               'sub_1': sub_1,
               'sub_2': sub_2,
               'sub_3': sub_3,
               }
    return render(request, 'login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Поздравляем! Вы успешно зарегистрированы!')
            return HttpResponseRedirect(reverse('users:login'))
        else:
            print(form.errors)
    else:
        form = UserRegistrationForm()
    subcategories = Subcategory.objects.all()
    sub_1 = subcategories[0:4]
    sub_2 = subcategories[4:7]
    sub_3 = subcategories[6]
    context = {'form': form,
               'sub_1': sub_1,
               'sub_2': sub_2,
               'sub_3': sub_3,
               }
    return render(request, 'registration1.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
    baskets = Basket.objects.filter(user=request.user)[:4]
    subcategories = Subcategory.objects.all()
    sub_1 = subcategories[0:4]
    sub_2 = subcategories[4:7]
    sub_3 = subcategories[6]
    context = {'title': 'Store - Профиль',
               'user_form': user_form,
               'profile_form': profile_form,
               'baskets': baskets,
               'sub_1': sub_1,
               'sub_2': sub_2,
               'sub_3': sub_3,
               }
    return render(request, 'profile1.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('products:index'))



