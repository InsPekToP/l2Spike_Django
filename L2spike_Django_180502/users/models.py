from django.db import models


class TestUser(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128)

    class Meta:
        app_label = 'users'  # имя твоего приложения
        db_table = 'accounts'
        managed = False
