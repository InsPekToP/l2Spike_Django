from django.shortcuts import render,redirect
from . forms import UserRegisterForm
from django.contrib import messages

from users.models import TestUser


# from django.contrib.auth.forms import UserCreationForm

# def register(request):
#     form = UserCreationForm()
#     context ={
#         'title' : 'Регистрация • L2Spike',
#         'form' : form
#         }
#     return render(request,'users/registration.html', context)


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            TestUser.objects.using('test').create(
                username=username,
                password=password
            )

            messages.success(request,f'Пользователь {username} был успешно создан!')
            return redirect('home')
        

            

    else:
        form = UserRegisterForm()
    return render(
        request,
        'users/registration.html',
        {
            'title':'Страница регистрации',
            'form':form
            }
        )