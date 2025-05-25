from django.shortcuts import render


def register(request):
    context ={
            'title' : 'Регистрация • L2Spike'
            }
    return render(request,'users/registration.html', context)