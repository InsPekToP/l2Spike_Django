from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse('<h3>Главная страница</h3>')


def about(request):
    return HttpResponse('<h3>О сервере </h3>')


def news(request):
    return HttpResponse('<h3>Новости</h3>')