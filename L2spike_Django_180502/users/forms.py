from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
    PasswordChangeForm
    )


class UserRegisterForm(UserCreationForm):
    login = forms.CharField(
        label = 'Введите логин',
        required = True,
        max_length = 14,
        # help_text ='Нельзя вводить символы: @,/,&,!,?',
        widget = forms.TextInput(attrs={'class':'input-field', 'placeholder':'Введите логин'})
    )
    email = forms.EmailField(
        label = 'Введите Email',
        required = True,
        #Уникальный или нет эмеил
        max_length = 100,
        widget = forms.TextInput(attrs={'class':'input-field', 'placeholder':'Введите Email'})
    )
    password1 = forms.CharField(
        label = 'Введите пароль',
        required = True,
        strip=False,
        # help_text= 'Пароль не долженм быть коротким и простым',
        widget = forms.PasswordInput(attrs={'class':'input-field', 'placeholder':'Введите Пароль', 'data-password-toggle':'true'})
    )
    password2 = forms.CharField(
        label = 'Потвердите пароль',
        required = True,
        strip=False,
        widget = forms.PasswordInput(attrs={'class':'input-field', 'placeholder':'Подтвердите Пароль', 'data-password-toggle':'true'})
    )


    class Meta:
        model = User
        fields = ['login','email','password1','password2']


    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if User.objects.filter(email__iexact=email).exists():
    #         raise ValidationError('Этот email уже используется.')
    #     return email

    #теперь email считается занятым только если пользователь активирован
    def clean_email(self):
        email = self.cleaned_data.get('email')
        existing_user = User.objects.filter(email__iexact=email, is_active=True).first()
        if existing_user:
            raise ValidationError('Этот email уже используется.')
        return email

    
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data['login']  # 👈 ключевая строка
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    

#Авторизация пользователя(Логин и пароль)
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label ='Введите логин',
        required = True,
        max_length = 14,
        widget = forms.TextInput(attrs={'class':'input-field','placeholder':'Введите логин'})
    )

    password = forms.CharField(
        label = 'Введите пароль',
        required = True,
        strip=False,
        widget = forms.PasswordInput(attrs={'class':'input-field','placeholder':'Введите пароль', 'data-password-toggle':'true'})
    )

#Смена пароля для неавторизированного поль-ля
class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label = 'Введите Email',
        required = True,
        max_length = 100,
        widget = forms.TextInput(attrs={'class':'input-field', 'placeholder':'Введите Email'})
    )
        

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError("Пользователь с таким email не зарегистрирован.")
        return email
        

#Смена пароля для неавторизированного поль-ля
class UserSetPasswordForm(SetPasswordForm):
        new_password1 = forms.CharField(
            label="Новый пароль",
            required = True,
            strip = False,
            widget = forms.PasswordInput(attrs={
                'class': 'input-field',
                'placeholder': 'Введите новый пароль',
                'data-password-toggle': 'true'
            }),
        )

        new_password2 = forms.CharField(
            label='Подтвердите пароль',
            required= True,
            strip=False,
            widget=forms.PasswordInput(attrs={
                 'class': 'input-field',
                 'placeholder': 'Подтвердите пароль',
                 'data-password-toggle': 'true'
            }),
        )

#Смена пароля для авторизированного поль-ля из ЛК(без эмейла)
class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Текущий пароль",
        required= True,
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Старый пароль','data-password-toggle': 'true'})
    )
    new_password1 = forms.CharField(
        label="Новый пароль",
        required= True,
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Новый пароль','data-password-toggle': 'true'})
    )
    new_password2 = forms.CharField(
        label="Подтвердите новый пароль",
        required= True,
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Повторите пароль','data-password-toggle': 'true'})
    )