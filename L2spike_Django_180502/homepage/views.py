from django.shortcuts import render


def home(request):
    return render(request,'homepage/home.html')


def about(request):
    return render(request,'homepage/about.html')


def news(request):
    return render(request,'homepage/news.html')