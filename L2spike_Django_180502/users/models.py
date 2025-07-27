from django.db import models

from django.utils.timezone import now
import uuid



#Временное хранение,для активации емейла после перехода по ссылке
class PendingRegistration(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    login = models.CharField(max_length=50)
    encoded_password = models.CharField(max_length=128)
    created_at = models.DateTimeField(default=now)
    token = models.UUIDField(default=uuid.uuid4, unique=True)


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


class Characters (models.Model):
    account_name = models.CharField(max_length=45, default='', null=True)
    obj_Id = models.DecimalField(max_digits=11, decimal_places=0, primary_key=True, default=0)
    char_name = models.CharField(max_length=35)
    name_color = models.CharField(max_length=6, default='FFFFFF')
    level = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    maxHp = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    curHp = models.DecimalField(max_digits=18, decimal_places=0, null=True)
    maxCp = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    curCp = models.DecimalField(max_digits=18, decimal_places=0, null=True)
    maxMp = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    curMp = models.DecimalField(max_digits=18, decimal_places=0, null=True)
    acc = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    crit = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    evasion = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    mAtk = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    mDef = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    mSpd = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    pAtk = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    pDef = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    pSpd = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    runSpd = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    walkSpd = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    str = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    con = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    dex = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    # _int = models.DecimalField(max_digits=11, decimal_places=0, null=True, db_column='int')
    men = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    wit = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    face = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    hairStyle = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    hairColor = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    sex = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    heading = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    x = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    y = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    z = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    movement_multiplier = models.DecimalField(max_digits=9, decimal_places=8, null=True)
    attack_speed_multiplier = models.DecimalField(max_digits=10, decimal_places=9, null=True)
    colRad = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    colHeight = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    exp = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    expBeforeDeath = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    sp = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    karma = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    pvpkills = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    pkkills = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    clanid = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    maxload = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    race = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    classid = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    base_class = models.IntegerField(default=0)
    deletetime = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    cancraft = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    title = models.CharField(max_length=16, null=True)
    title_color = models.CharField(max_length=6, default='FFFF77')
    rec_have = models.IntegerField(default=0)
    rec_left = models.IntegerField(default=0)
    accesslevel = models.DecimalField(max_digits=4, decimal_places=0, null=True)
    online = models.DecimalField(max_digits=1, decimal_places=0, null=True)
    onlinetime = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    char_slot = models.DecimalField(max_digits=1, decimal_places=0, null=True)
    newbie = models.DecimalField(max_digits=1, decimal_places=0, default=1)
    lastAccess = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    clan_privs = models.IntegerField(default=0)
    wantspeace = models.DecimalField(max_digits=1, decimal_places=0, default=0)
    isin7sdungeon = models.DecimalField(max_digits=1, decimal_places=0, default=0)
    in_jail = models.DecimalField(max_digits=1, decimal_places=0, null=True)
    jail_timer = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    power_grade = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    nobless = models.DecimalField(max_digits=1, decimal_places=0, default=0)
    subpledge = models.IntegerField(default=0)
    last_recom_date = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    lvl_joined_academy = models.IntegerField(default=0)
    apprentice = models.IntegerField(default=0)
    sponsor = models.IntegerField(default=0)
    varka_ketra_ally = models.IntegerField(default=0)
    clan_join_expiry_time = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    clan_create_expiry_time = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    lang = models.CharField(max_length=2, null=True)
    chatban_timer = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    death_penalty_level = models.IntegerField(default=0)
    isKillerPlayer = models.IntegerField(default=0)
    ban_timer = models.IntegerField(default=0)
    hero = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    hero_aura = models.CharField(max_length=45, default='0')
    BanReason = models.CharField(max_length=250, default='0')
    premium = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    chatban_reason = models.CharField(max_length=255, default='')
    chat_filter_count = models.CharField(max_length=45, default='0')
    lastteleport = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    deaths = models.DecimalField(max_digits=11, decimal_places=0, default=0)

    class Meta:
        app_label = 'users'
        db_table = 'characters'
        verbose_name = 'Character'
        verbose_name_plural = 'Characters'
        managed = False

    def __str__(self):
        return self.char_name