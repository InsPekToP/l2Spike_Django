from django.db import models


# class TestUser(models.Model):
#     username = models.CharField(max_length=150)
#     password = models.CharField(max_length=128)

#     class Meta:
#         app_label = 'users'  # имя твоего приложения
#         db_table = 'accounts'
#         managed = False



class Accounts(models.Model):
    login = models.CharField(max_length=45, primary_key=True, default='')
    password = models.CharField(max_length=45, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    lastactive = models.BigIntegerField(default=0)
    accessLevel = models.PositiveSmallIntegerField(default=0)
    lastIP = models.CharField(max_length=15, null=True, blank=True)
    lastServer = models.PositiveSmallIntegerField(default=1, null=True, blank=True)
    pcIp = models.CharField(max_length=15, null=True, blank=True)
    hop1 = models.CharField(max_length=15, null=True, blank=True)
    hop2 = models.CharField(max_length=15, null=True, blank=True)
    hop3 = models.CharField(max_length=15, null=True, blank=True)
    hop4 = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        app_label = 'users'  # имя твоего приложения
        db_table = 'accounts'
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        # managed = False

    def __str__(self):
        return self.login