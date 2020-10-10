from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

from scraping.models import Location, Specialty

User = get_user_model()


class UserAuthenticateForm(forms.Form):
    email = forms.EmailField(
        label=False,
        widget=forms.EmailInput(attrs={'class': 'form-control',
                                       'placeholder': 'Введите email'})
    )
    password = forms.CharField(
        label=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Введите пароль'})
    )

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email').strip()
        password = self.cleaned_data.get('password').strip()

        if email and password:
            user_account = User.objects.filter(email=email)

            if not user_account.exists():
                raise forms.ValidationError('Такого пользователя нет')

            if not check_password(password, user_account[0].password):
                raise forms.ValidationError('Неверный пароль')

            user = authenticate(email=email, password=password)

            if not user:
                raise forms.ValidationError('Данный аккаунт отключен')
        return super(UserAuthenticateForm, self).clean()


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(
        label=False,
        widget=forms.EmailInput(attrs={'class': 'form-control',
                                       'placeholder': 'Введите email'})
    )
    password1 = forms.CharField(
        label=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Введите пароль'})
    )
    password2 = forms.CharField(
        label=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Введите пароль '
                                                         'еще раз'})
    )

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        data = self.cleaned_data
        if data['password1'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return data['password2']


class UserUpdateForm(forms.Form):
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        to_field_name='slug',
        required=True,
        label=False,
        empty_label='Выберите город',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    specialty = forms.ModelChoiceField(
        queryset=Specialty.objects.all(),
        to_field_name='slug',
        required=True,
        label=False,
        empty_label='Выберите специальность',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    is_subscriber = forms.BooleanField(
        required=False,
        label='Подписка',
        widget=forms.CheckboxInput
    )

    class Meta:
        model = User
        fields = ('location', 'specialty', 'is_subscriber')
