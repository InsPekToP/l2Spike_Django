from django.shortcuts import render


def home(request):

    context ={
            'title' : 'L2Spike • Interlude • x50.000'
            }


    return render(request,'homepage/home.html', context)


def about(request):

    context = {
        
            'title' : 'L2Spike •  Описание сервера • Interlude • x50.000'
        }

    return render(request,'homepage/about.html', context)


def news(request):

    context = {
            'title' : 'L2Spike • Новости • Interlude • x50.000'
        }

    return render(request,'homepage/news.html', context)