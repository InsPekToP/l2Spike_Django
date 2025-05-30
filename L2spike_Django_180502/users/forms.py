from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    login = forms.CharField(
        label = 'Введите логин',
        required = True,
        max_length = 14,
        # help_text ='Нельзя вводить символы: @,/,&,!,?',
        widget = forms.TextInput(attrs={'class':'form-control', 'placeholder':'Введите логин'})
    )
    email = forms.EmailField(
        label = 'Введите Email',
        required = True,
        max_length = 100,
        widget = forms.TextInput(attrs={'class':'form-control', 'placeholder':'Введите Email'})
    )
    password1 = forms.CharField(
        label = 'Введите пароль',
        required = True,
        # help_text= 'Пароль не долженм быть коротким и простым',
        widget = forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Введите Пароль'})
    )
    password2 = forms.CharField(
        label = 'Потвердите пароль',
        required = True,
        widget = forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Введите Пароль'})
    )


    class Meta:
        model = User
        fields = ['login','email','password1','password2']

    
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data['login']  # 👈 ключевая строка
        # user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user