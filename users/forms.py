from django import forms
from .models import Order
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from phonenumber_field.formfields import PhoneNumberField


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем атрибуты ко всем полям
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class UserCreateForm(BootstrapFormMixin, UserCreationForm):
    username = forms.CharField(label='Логин*')
    password1 = forms.CharField(label='Пароль*', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повтор пароля*', widget=forms.PasswordInput())
    email = forms.EmailField(label='E-mail*')
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            }


class UserLoginForm(BootstrapFormMixin, AuthenticationForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class UserUpdateForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']

        labels = {
            "username": "Логин",
            "email": "Эл. почта",
            "first_name": "Имя",
            "last_name": "Фамилия"
            }

        widgets = {
            "username": forms.TextInput(attrs={"style": "width: 230px;", "disabled": True}),
            "email": forms.TextInput(attrs={"disabled": True}),
            }


class UserPasswordChangeForm(BootstrapFormMixin, PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput())
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput())
    new_password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput())


class OrderForm(BootstrapFormMixin, forms.ModelForm):
    phone = PhoneNumberField(
        widget=forms.TextInput(attrs={'placeholder': '+7XXXXXXXXXX', 'style': 'width: 200px'}),
        region='RU',  # Указываем регион для валидации
        label="Номер телефона"
    )
    address = forms.CharField(label="Адрес", widget=forms.Textarea(attrs={'style': 'height: 100px; width: 300px;'}))

    class Meta:
        model = Order
        fields = ['phone', 'address']