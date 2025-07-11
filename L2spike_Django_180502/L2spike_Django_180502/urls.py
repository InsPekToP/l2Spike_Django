"""
URL configuration for L2spike_Django_180502 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from users import views as userViews
from users.forms import UserLoginForm
from django.contrib.auth import views as authViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('', include('users.urls')),
    path('profile/', userViews.profile, name='profile'),
    # path('login/', authViews.LoginView.as_view(template_name = 'users/login.html'), name = 'login'),
    path('login/', authViews.LoginView.as_view(template_name = 'users/login.html',authentication_form=UserLoginForm), name = 'login'),
    path('exit/', authViews.LogoutView.as_view(template_name = 'users/exit.html'), name = 'exit'),

    path('pass-reset/', authViews.PasswordResetView.as_view(template_name = 'users/pass_reset.html'),name='pass-reset'),
    #эту страничку будем показывать в самую последнюю очередь
    path('password_reset_complete/',authViews.PasswordResetCompleteView.as_view(template_name = 'users/password_reset_complete.html'),name='password_reset_complete'),
    #отслеживание востановление пароля
    path('password_reset_confirm/<uidb64>/<token>/',authViews.PasswordResetConfirmView.as_view(template_name = 'users/password_reset_confirm.html'),name='password_reset_confirm'),
    #отслеживание отправку емейла на востановление пароля
    path('password_reset_done/',authViews.PasswordResetDoneView.as_view(template_name = 'users/password_reset_done.html'),name='password_reset_done'),  
]
