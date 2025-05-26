from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def register(request):
    form = UserCreationForm()
    context ={
        'title' : 'Регистрация • L2Spike',
        'form' : form
        }
    return render(request,'users/registration.html', context)