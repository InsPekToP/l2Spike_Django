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
from django.contrib.auth import views as authViews
from users.forms import (
    UserLoginForm,
    UserPasswordResetForm,
    UserSetPasswordForm,
    UserPasswordChangeForm
    )

# from users.views import (
#     CustomPasswordResetConfirmView,
#     CustomPasswordChangeView,
#     CustomPasswordResetView
#     )



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('', include('users.urls')),
    path('profile/', userViews.profile, name='profile'),
    # path('login/', authViews.LoginView.as_view(template_name = 'users/login.html'), name = 'login'),
    path('login/', authViews.LoginView.as_view(template_name = 'users/login.html',authentication_form=UserLoginForm), name = 'login'),
    path('exit/', authViews.LogoutView.as_view(template_name = 'users/exit.html'), name = 'exit'),

    #Потверждение емейла
    path('activate/<uidb64>/<token>/', userViews.activate_account, name='activate_account'),

    #Первая страничка(на смену пароля не авторизированного пользователя) с вводом эмейла
    #(Стандартная вьюха,Стандартная форма)
    # path('pass-reset/', authViews.PasswordResetView.as_view(template_name = 'users/pass_reset.html'),name='pass-reset'),

    #(Стандартная вьюха,Кастомная форма)
    # path('pass-reset/', authViews.PasswordResetView.as_view(
    #         template_name = 'users/pass_reset.html',
    #         form_class=UserPasswordResetForm
    #     ),
    #     name='pass-reset'
    # ),

    #(Кастомная вьюха,Кастомная форма)
    path('pass-reset/', userViews.CustomPasswordResetView.as_view(
            template_name = 'users/pass_reset.html',
            form_class=UserPasswordResetForm
        ),
        name='pass-reset'
    ),

    #Вторая страничка с инфой,что письмо отправлено
    path('password_reset_done/',authViews.PasswordResetDoneView.as_view(template_name = 'users/password_reset_done.html'),name='password_reset_done'),

    #Третья страничка(после перехода по ссылке из эмейла) с двумя полями ввода нового пароля(Стандартная вьюха,Стандартная форма)
    # path('password_reset_confirm/<uidb64>/<token>/',authViews.PasswordResetConfirmView.as_view(template_name = 'users/password_reset_confirm.html'),name='password_reset_confirm'),

    #(Стандартная вьюха,Кастомная форма)
    # path('password_reset_confirm/<uidb64>/<token>/',authViews.PasswordResetConfirmView.as_view(
    #     template_name = 'users/password_reset_confirm.html',
    #     form_class=UserSetPasswordForm
    #     ),
    #     name='password_reset_confirm'
    # ),

    #(Кастомная вьюха,Кастомная форма)
    path('password_reset_confirm/<uidb64>/<token>/', userViews.CustomPasswordResetConfirmView.as_view(
    template_name = 'users/password_reset_confirm.html',
    form_class=UserSetPasswordForm
    ),
    name='password_reset_confirm'
    ),
    
    #Четвертая страничка с инфой,что пароль обновлен
    path('password_reset_complete/',authViews.PasswordResetCompleteView.as_view(template_name = 'users/password_reset_complete.html'),name='password_reset_complete'),

    #Смена пароля внутри ЛК(Стандартная вьюха,Стандартная форма)
    # path('password-change/', authViews.PasswordChangeView.as_view(template_name='users/password_change.html'), name='password_change'),

    #(Стандартная вьюха,Кастомная форма)
    # path('password-change/', authViews.PasswordChangeView.as_view(
    #     template_name='users/password_change.html',
    #     form_class=UserPasswordChangeForm
    #     ),
    #     name='password_change'),

    #(Кастомная вьюха,Кастомная форма)
    path('password-change/', userViews.CustomPasswordChangeView.as_view(
    template_name='users/password_change.html',
    form_class=UserPasswordChangeForm
    ),
    name='password_change'),

    #Редирект после смены пароля
    path('password-change-done/', authViews.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),

    #Повторная отправка ссылки
    path('resend-activation/', userViews.resend_activation_email, name='resend_activation_email'),
]
