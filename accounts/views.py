from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages

from accounts.forms import (
    UserAuthenticateForm, UserRegistrationForm, UserUpdateForm
)
User = get_user_model()


def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password2'])
        new_user.save()
        messages.success(request, 'Пользователь добавлен в систему.')
        return render(
            request,
            'accounts/registration_account_successful.html',
            {'user': new_user})
    return render(request, 'accounts/registration_page.html', {'form': form})


def login_view(request):
    form = UserAuthenticateForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'accounts/login_page.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def update_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user.city = data['city']
                user.language = data['language']
                user.email_subscription = data['email_subscription']
                user.save()
                return redirect('accounts:update')
        form = UserUpdateForm(initial={
            'city': user.city,
            'language': user.language,
            'email_subscription': user.email_subscription})
        return render(
            request,
            'accounts/settings_update_page.html', {'form': form})
    else:
        return redirect('accounts:login')


def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            user_object = User.objects.get(pk=user.pk)
            user_object.delete()
        return render(
            request,'accounts/delete_account_successful.html', {'user': user})
    else:
        return redirect('home')
