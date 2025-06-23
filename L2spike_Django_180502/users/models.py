from django.db import models


class Accounts(models.Model):
    login = models.CharField(max_length=45, primary_key=True, default='')
    password = models.CharField(max_length=45, default='')
    lastactive = models.BigIntegerField(default=0)
    access_level = models.SmallIntegerField(default=0)
    lastIP = models.CharField(max_length=15, default='')
    lastServer = models.PositiveSmallIntegerField(default=1)
    email = models.CharField(max_length=50, default='')
    BanReason = models.CharField(max_length=250, default='')
    question1 = models.CharField(max_length=250, default=' ')
    answer1 = models.CharField(max_length=250, default=' ')
    question2 = models.CharField(max_length=250, default=' ')
    answer2 = models.CharField(max_length=250, default=' ')
    l2answer = models.CharField(max_length=100, default='')
    l2question = models.CharField(max_length=100, default='')
    l2email = models.CharField(max_length=100, default='null@null')
    hwid = models.CharField(max_length=100, default='')
    last_hwid = models.CharField(max_length=100, default='')

    class Meta:
        app_label = 'users'
        db_table = 'accounts'
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        managed = False

    def __str__(self):
        return self.login
