from django.contrib import messages
from django.contrib.auth import login as auth_login,get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.timezone import now
from django.utils.dateparse import parse_datetime
# from django.contrib.auth.tokens import default_token_generator
from .tokens import email_token_generator
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm
from users.models import Accounts, Characters
from .utils import send_activation_email

#импорты для смены пароля через емейл
from django.contrib.auth.views import PasswordResetConfirmView,PasswordChangeView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

import hashlib
import base64
from datetime import timedelta



def register(request):
    context = {
        'title': 'L2Spike • Регистрация • Interlude • x50.000'
    }

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data.get('login') or form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')

            try:
                #Проверка: есть ли пользователь с таким email, но не активирован
                existing_user = User.objects.filter(email__iexact=email, is_active=False).first()
                if existing_user:
                    sha_hash = hashlib.sha1(password.encode('utf-8')).digest()
                    encoded_password = base64.b64encode(sha_hash).decode('utf-8')

                    send_activation_email(request, existing_user)
                    request.session['encoded_password'] = encoded_password

                    messages.info(request, f"Пользователь с этим email уже зарегистрирован, но не активирован. Мы повторно отправили ссылку для активации.")
                    return render(request, 'users/send_email.html', {'email': email})


                # Проверка на существование логина в Accounts (в тестовой БД)
                if not Accounts.objects.using('test').filter(login=login).exists():
                    # Хешируем пароль
                    sha_hash = hashlib.sha1(password.encode('utf-8')).digest()
                    encoded_password = base64.b64encode(sha_hash).decode('utf-8')

                    # Создаем пользователя Django
                    user = form.save(commit=False)
                    user.is_active = False
                    user.save()

                    #Отправляем потверждение на email
                    send_activation_email(request, user)

                    #Засекает время для повторной отправки емейла
                    request.session['last_activation_email_sent'] = now().isoformat()

                    #Автоматически логиним пользователя
                    # auth_login(request, user)

                    # Создаем запись в Accounts
                    # Accounts.objects.using('test').create(
                    #     login=login,
                    #     password=encoded_password,
                    #     # email=form.cleaned_data.get('email')
                    # )

                    # messages.success(request, f'Перейдите по ссылке в email для активации аккаунта.')
                    # return redirect('profile')

                    # Сохраняем пароль в сессию (на время)
                    request.session['encoded_password'] = encoded_password

                    return render(request, 'users/send_email.html', {'email': user.email})

                else:
                    messages.error(request, f'Логин {login} уже используется')
                    return redirect('reg')
                

            except IntegrityError:
                messages.error(request, f'Ошибка при создании пользователя {login}.')
                return redirect('reg')
        
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



#Повторная отправка ссылки
def resend_activation_email(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = User.objects.filter(email__iexact=email, is_active=False).first()

        if not user:
            messages.error(request, "Пользователь с таким email не найден или уже активирован.")
            return redirect('reg')

        # Проверка частоты (5 минут)
        last_sent = request.session.get('last_activation_email_sent')
        if last_sent:
            last_sent_dt = parse_datetime(last_sent)
            if now() - last_sent_dt < timedelta(minutes=5):
                remaining = 300 - int((now() - last_sent_dt).total_seconds())
                minutes, seconds = divmod(remaining, 60)
                messages.warning(request, f"Вы уже запрашивали письмо недавно. Подождите ещё {minutes} мин {seconds} сек.")
                return render(request, 'users/send_email.html', {'email': email})

        # Отправляем повторно
        send_activation_email(request, user)

        # Обновляем сессию с меткой времени
        request.session['last_activation_email_sent'] = now().isoformat()

        messages.success(request, f"Письмо подтверждения повторно отправлено на {email}.")
        return render(request, 'users/send_email.html', {'email': email})

    return redirect('reg')




def activate_account(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    # if user and default_token_generator.check_token(user, token):
    if user and email_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        # Синхронизируем в test-БД только сейчас:
        # sha_hash = hashlib.sha1(user.password.encode('utf-8')).digest()
        # encoded_password = base64.b64encode(sha_hash).decode('utf-8')

        # Берем хеш из сессии
        encoded_password = request.session.get('encoded_password')

        if encoded_password:
            Accounts.objects.using('test').create(
                login=user.username,
                password=encoded_password,
            )
            # Можно удалить из сессии, чтобы не осталось
            del request.session['encoded_password']
        else:
            messages.warning(request, "Не удалось синхронизировать аккаунт")

        # Авто-логин
        auth_login(request, user)

        messages.success(request, f"Аккаунт {user.username} успешно активирован! Добро пожаловать")
        return redirect('profile')
    else:
        messages.error(request, 'Ссылка для активации недействительна или устарела.')
        return redirect('reg')


@login_required
def profile(request):
    user = request.user
    # print("Django username:", user.username)  # ← Проверка
    
    try:
        #Получаем аккаунт из второй БД(test) по логину пользователя Django
        account = Accounts.objects.using('test').get(login=user.username)
        # print("Accounts login:", account.login)  # ← Проверка
    except Accounts.DoesNotExist:
        account = None

    characters = []
    if account:
        #Получаем персонажей,связаных с аккаунтом(тоже из второй БД)
        characters = Characters.objects.using('test').filter(account_name=account.login)

    return render(request, 'users/profile.html',{
        'user': user,
        'account': account,
        'characters': characters,
    })



#Смена пароля для неавторизированных пользователей(через емейл)
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)

        # 👇 После обновления пароля в Django — получаем пользователя
        user = self.user

        try:
            # Обновляем пароль в test-базе (модель Accounts)
            login = user.username  # используешь login как username

            new_password = form.cleaned_data.get('new_password1')
            sha_hash = hashlib.sha1(new_password.encode('utf-8')).digest()
            encoded_password = base64.b64encode(sha_hash).decode('utf-8')

            updated = Accounts.objects.using('test').filter(login=login).update(password=encoded_password)

            if updated == 0:
                messages.warning(self.request, f'Внимание: логин {login} не найден в базе.')
            else:
                messages.success(self.request, 'Пароль обновлён и синхронизирован с игрой.')

        except Exception as e:
            messages.error(self.request, f'Ошибка при обновлении пароля в базе: {e}')

        return response
    


#Смена пароля для авторизированных пользователей(через ЛК)
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'users/password_change.html'  # путь к твоему шаблону
    success_url = reverse_lazy('password_change_done')  # перенаправление после смены пароля

    def form_valid(self, form):
        response = super().form_valid(form)

        user = self.request.user
        login = user.username
        new_password = form.cleaned_data.get('new_password1')

        try:
            sha_hash = hashlib.sha1(new_password.encode('utf-8')).digest()
            encoded_password = base64.b64encode(sha_hash).decode('utf-8')

            updated = Accounts.objects.using('test').filter(login=login).update(password=encoded_password)

            if updated == 0:
                messages.warning(self.request, f'Внимание: логин {login} не найден.')
            else:
                messages.success(self.request, 'Пароль успешно обновлён и синхронизирован с игрой.')

        except Exception as e:
            messages.error(self.request, f'Ошибка при обновлении пароля: {e}')

        return response