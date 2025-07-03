from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from users.models import Accounts
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

import hashlib
import base64


def register(request):
    context = {
        'title': 'L2Spike • Регистрация • Interlude • x50.000'
    }

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data.get('login') or form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            try:
                # Проверка на существование логина в Accounts (в тестовой БД)
                if not Accounts.objects.using('test').filter(login=login).exists():
                    # Хешируем пароль
                    sha_hash = hashlib.sha1(password.encode('utf-8')).digest()
                    encoded_password = base64.b64encode(sha_hash).decode('utf-8')

                    # Создаем пользователя Django
                    user = form.save()

                    # Создаем запись в Accounts
                    Accounts.objects.using('test').create(
                        login=login,
                        password=encoded_password,
                        # email=form.cleaned_data.get('email')
                    )

                else:
                    messages.error(request, f'Логин {login} уже используется')
                    return redirect('reg')
                

            except IntegrityError:
                messages.error(request, f'Ошибка при создании пользователя {login}.')
                return redirect('reg')

            messages.success(request, f'Пользователь {login} был успешно создан!')
            return redirect('home')
        
        
        else:
            # Форма невалидна — показать ошибки на странице
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")


    else:
        form = UserRegisterForm()
    context['form'] = form  # Добавляем форму в контекст
    # return render(request, 'users/registration.html', {'form': form})
    return render(request, 'users/registration.html', context)


@login_required
def profile(request):
    return render(request, 'users/profile.html')