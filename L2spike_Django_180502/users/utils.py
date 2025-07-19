from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
# from django.contrib.auth.tokens import default_token_generator
from .tokens import email_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse




def send_activation_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    # token = default_token_generator.make_token(user)
    token = email_token_generator.make_token(user)
    activation_url = request.build_absolute_uri(
        reverse('activate_account', kwargs={'uidb64': uid, 'token': token})
    )

    subject = 'Подтверждение регистрации на L2Spike.com'
    html_message = render_to_string('users/activation_email.html', {
        'user': user,
        'activation_url': activation_url,
    })
    plain_message = f"Привет, {user.username}!\n\nПерейди по ссылке, чтобы активировать аккаунт:\n{activation_url}"

    send_mail(subject, plain_message, 'noreply@l2spike.com', [user.email],html_message=html_message)