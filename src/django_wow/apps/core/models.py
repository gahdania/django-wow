from django.db import models
from apps.users.models import User, Region, Locale, Account
from django.core.files.storage import FileSystemStorage
from django.conf import settings


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'users/{instance.user.id}/{filename}'


spec_storage = FileSystemStorage(location=f"{settings.STATIC_ROOT}/icons/specs/", base_url="/static/icons/spec")


class_storage = FileSystemStorage(location=f"{settings.STATIC_ROOT}/icons/class/", base_url="/static/icons/class")


class Gender(models.Model):
    slug = models.CharField(max_length=20)
    gender_id = models.PositiveSmallIntegerField(default=0)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug


class GenderName(models.Model):
    name = models.CharField(max_length=20)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    locale = models.ForeignKey(Locale, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('gender', 'locale')

    def __str__(self):
        return self.name


class RealmType(models.Model):
    slug = models.SlugField(max_length=20)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug


class RealmTypeName(models.Model):
    realm_type = models.ForeignKey(RealmType, on_delete=models.DO_NOTHING)
    locale = models.ForeignKey(Locale, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=20, blank=True, default='')

    def __str__(self):
        return self.name


class Realm(models.Model):
    slug = models.SlugField(max_length=100)
    last_updated = models.DateTimeField(auto_now=True)
    realm_id = models.PositiveIntegerField(primary_key=True)
    timezone = models.CharField(max_length=50)
    type = models.ForeignKey(RealmType, on_delete=models.DO_NOTHING)
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING)
    is_tournament_realm = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.slug} - {self.region.tag}"

    class Meta:
        unique_together = ('realm_id', 'region')

    def localize(self, user_id):
        user = User.objects.get(pk=user_id)
        return self.realmname_set.get(locale=user.preferred_locale)

    @property
    def display_name(self):
        return f"{self.slug} - {self.region.tag.upper()}"


class RealmName(models.Model):
    locale = models.ForeignKey(Locale, on_delete=models.DO_NOTHING)
    realm = models.ForeignKey(Realm, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('locale', 'realm')

    def __str__(self):
        return self.name


class ConnectedRealm(models.Model):
    connected_realm_id = models.PositiveIntegerField(default=0, primary_key=True)
    connected_realms = models.ManyToManyField(Realm)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.connected_realms[0].slug


class Faction(models.Model):

    slug = models.SlugField(max_length=30)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug


class FactionName(models.Model):

    faction = models.ForeignKey(Faction, on_delete=models.DO_NOTHING)
    locale = models.ForeignKey(Locale, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class PlayableClass(models.Model):
    slug = models.SlugField(max_length=50)
    class_id = models.PositiveIntegerField(primary_key=True)
    icon = models.ImageField(blank=True, null=True, storage=class_storage)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Playable Classes'

    def __str__(self):
        return self.slug


class ClassName(models.Model):
    male = models.CharField('Masculine Name', max_length=50, default='', blank=True, null=True)
    female = models.CharField('Feminine Name', max_length=50, default='', blank=True, null=True)
    name = models.CharField('Generic Name', max_length=50, default='', blank=True, null=True)
    locale = models.ForeignKey(Locale, on_delete=models.DO_NOTHING)
    cls = models.ForeignKey(PlayableClass, verbose_name='Class', on_delete=models.DO_NOTHING)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('locale', 'cls')

    def __str__(self):
        return self.male


class Spec(models.Model):
    slug = models.SlugField(max_length=50)
    spec_id = models.PositiveIntegerField(primary_key=True)
    icon = models.ImageField(blank=True, null=True, storage=spec_storage)
    cls = models.ForeignKey(PlayableClass, verbose_name='Class', on_delete=models.DO_NOTHING)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Playable Specialization'

    def __str__(self):
        return self.slug


class SpecName(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    male = models.TextField('Male description', max_length=50, default='', blank=True, null=True)
    female = models.TextField('Female description', max_length=50, default='', blank=True, null=True)
    locale = models.ForeignKey(Locale, on_delete=models.DO_NOTHING)
    spec = models.ForeignKey(Spec, on_delete=models.DO_NOTHING)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('locale', 'spec')

    def __str__(self):
        return self.name


class Race(models.Model):

    slug = models.SlugField()
    race_id = models.PositiveIntegerField(primary_key=True)
    last_updated = models.DateTimeField(auto_now=True)
    faction = models.ForeignKey(Faction, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.slug


class RaceName(models.Model):
    male = models.CharField('Masculine Name', max_length=50, default='', blank=True, null=True)
    female = models.CharField('Feminine Name', max_length=50, default='', blank=True, null=True)
    name = models.CharField('Generic Name', max_length=50, default='', blank=True, null=True)
    locale = models.ForeignKey(Locale, on_delete=models.DO_NOTHING)
    race = models.ForeignKey(Race, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ('locale', 'race')

    def __str__(self):
        return self.male


class Stat(models.Model):
    slug = models.CharField(verbose_name='Stat Slug', max_length=25)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug


class StatName(models.Model):
    stat = models.ForeignKey(Stat, on_delete=models.DO_NOTHING)
    locale = models.ForeignKey(Locale, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Character(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Blizzard Account')
    avatar = models.URLField()
    inset = models.URLField()
    main = models.URLField()
    raw = models.URLField()
    character_id = models.PositiveIntegerField(blank=True, null=True, default=None)
    name = models.CharField(max_length=50)
    realm = models.ForeignKey(Realm, on_delete=models.DO_NOTHING)
    last_updated = models.DateTimeField()
    created = models.DateTimeField(blank=True, null=True)
    race = models.ForeignKey(Race, on_delete=models.DO_NOTHING)
    cls = models.ForeignKey(PlayableClass, verbose_name='Class', on_delete=models.DO_NOTHING)
    level = models.PositiveSmallIntegerField(default=1)
    gender = models.ForeignKey(Gender, on_delete=models.DO_NOTHING)
    guild_rank = models.ForeignKey('GuildRank', on_delete=models.DO_NOTHING, null=True, blank=True)
    current_spec = models.ForeignKey(Spec, on_delete=models.DO_NOTHING)
    main_character = models.BooleanField(verbose_name='Main Character', default=False)

    def __str__(self):
        locale = Locale.objects.get(language='en', country='US')
        return f"{self.name} - {self.realm.realmname_set.get(locale=locale)}"


class GuildRank(models.Model):

    guild_rank = models.PositiveSmallIntegerField(default=0)
    name = models.CharField(max_length=100)
    guild = models.ForeignKey('Guild', on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.name} - {self.guild.__str__()}"


class Guild(models.Model):

    name = models.CharField(max_length=100)
    realm = models.ForeignKey(Realm, on_delete=models.DO_NOTHING)
    faction = models.ForeignKey(Faction, on_delete=models.DO_NOTHING)
    roster = models.ManyToManyField(Character, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(null=True, blank=True)  # pulled from API

    def __str__(self):
        return f"{self.name} - {self.realm}"
