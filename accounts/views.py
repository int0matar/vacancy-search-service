from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages

from accounts.forms import (
    UserAuthenticateForm, UserRegistrationForm, UserUpdateForm
)
User = get_user_model()


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


def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password2'])
        new_user.save()
        messages.success(request, 'Пользователь добавлен в систему.')
        return render(
            request,
            'accounts/registration_page_successful.html', {'user': new_user})
    return render(request, 'accounts/registration_page.html', {'form': form})
