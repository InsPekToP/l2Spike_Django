from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from users.models import Accounts
from django.contrib.auth.models import User
from django.db import IntegrityError

import hashlib
import base64


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data.get('login') or form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            if not login:
                messages.error(request, "Login/Username не может быть пустым.")
                return redirect('reg')

            # Проверка на существование логина в Django User
            # if User.objects.filter(username=login).exists():
            #     messages.error(request, f'Пользователь с логином {login} уже существует в системе.')
            #     return redirect('reg')

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

    return render(request, 'users/registration.html', {'form': form})



# def register(request):
#     if request.method == "POST":
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             login = form.cleaned_data.get('login')
#             password = form.cleaned_data.get('password1')

#             try:
#                 # Проверка на наличие в кастомной Accounts
#                 if not Accounts.objects.using('test').filter(login=login).exists():
#                     # Хешируем пароль
#                     sha_hash = hashlib.sha1(password.encode('utf-8')).digest()
#                     encoded_password = base64.b64encode(sha_hash).decode('utf-8')

#                     # Создаем пользователя Django
#                     user = form.save()

#                     # Создаем запись в Accounts
#                     Accounts.objects.using('test').create(
#                         login=login,
#                         password=encoded_password,
#                     )
#                 else:
#                     messages.error(request, f'Пользователь с логином {login} уже существует')
#                     return redirect('reg')

#             except IntegrityError:
#                 messages.error(request, f'Ошибка при создании пользователя {login}.')
#                 return redirect('reg')

#             messages.success(request, f'Пользователь {login} был успешно создан!')
#             return redirect('home')
#     else:
#         form = UserRegisterForm()

#     return render(request, 'users/registration.html', {'form': form})



# def register(request):
#     if request.method == "POST":
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             # Сохраняем пользователя Django
#             user = form.save()

#             # Получаем логин и пароль
#             login = form.cleaned_data.get('login') or form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')

#             # Проверка: login пустой?
#             if not login:
#                 messages.error(request, "Login/Username не может быть пустым.")
#                 return redirect('reg')

#             try:
#                 # Проверка: login уже есть в Accounts?
#                 if not Accounts.objects.using('test').filter(login=login).exists():
#                     # Хешируем пароль
#                     sha_hash = hashlib.sha1(password.encode('utf-8')).digest()
#                     encoded_password = base64.b64encode(sha_hash).decode('utf-8')

#                     Accounts.objects.using('test').create(
#                         login=login,
#                         password=encoded_password,  # в идеале — тоже хешировать или хранить как-то безопаснее
#                         # email=form.cleaned_data.get('email')
#                     )
#             except IntegrityError:
#                 messages.error(request, f'Пользователь с логином {login} уже есть в базе accounts (test).')
#                 return redirect('reg')

#             messages.success(request, f'Пользователь {login} был успешно создан!')
#             return redirect('home')
#     else:
#         form = UserRegisterForm()

#     return render(request, 'users/registration.html', {'form': form})




# from django.shortcuts import render,redirect
# from . forms import UserRegisterForm
# from django.contrib import messages

# from users.models import Accounts


# from django.contrib.auth.forms import UserCreationForm

# def register(request):
#     form = UserCreationForm()
#     context ={
#         'title' : 'Регистрация • L2Spike',
#         'form' : form
#         }
#     return render(request,'users/registration.html', context)


# def register(request):
#     if request.method == "POST":
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             login = form.cleaned_data.get('login')
#             password = form.cleaned_data.get('password1')

#             Accounts.objects.using('test').create(
#                 login=login,
#                 password=password
#             )

#             messages.success(request,f'Пользователь {login} был успешно создан!')
#             return redirect('home')
        

            

#     else:
#         form = UserRegisterForm()
#     return render(
#         request,
#         'users/registration.html',
#         {
#             'title':'Страница регистрации',
#             'form':form
#             }
#         )