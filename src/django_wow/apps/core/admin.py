from datetime import datetime
from io import BytesIO

from battlenet_client.wow.profile import profile, media_summary
from django.contrib import admin

from apps.users.views import oauth
from .models import (Character, Guild, GuildRank, Faction, FactionName, PlayableClass, ClassName, Spec, SpecName,
                     Race, RaceName, Realm, RealmName, Gender, GenderName)


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):

    list_display = ('name', 'realm', 'level', 'race', 'cls')
    list_filter = ('race', 'cls')

    change_fieldsets = (
        (None, {'fields': ('name', 'realm', 'main_character')}),
    )

    add_fieldsets = (
        (None, {'fields': ('user', 'name', 'realm', 'main_character')}),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            self.fieldsets = self.add_fieldsets
        else:
            self.fieldsets = self.change_fieldsets

        return super().get_fieldsets(request, obj)

    def save_model(self, request, obj, form, change):
        realm_slug = Realm.objects.get(realm_id=form['realm'].value()).slug
        url, params = profile(request.user.preferred_locale.region.tag, realm_slug,
                              form['name'].value(), locale=request.user.preferred_locale.__str__())
        char_data = oauth.battlenet.get(url, params=params).json()
        url, params = media_summary(request.user.preferred_locale.region.tag, realm_slug,
                                    form['name'].value(), locale=request.user.preferred_locale.__str__())
        media_data = oauth.battlenet.get(url, params=params).json()
        images = {}
        for asset in media_data['assets']:
            if asset['key'].endswith('raw'):
                images['raw'] = BytesIO(oauth.battlenet.client.get(asset['value'], params=params).content)
            else:
                images[asset['key']] = BytesIO(oauth.battlenet.client.get(asset['value'], params=params).content)

        obj.character_id = char_data['id']
        obj.name = char_data['name']
        obj.realm = Realm.objects.get(realm_id=char_data['realm']['id'])
        obj.race = Race.objects.get(race_id=char_data['race']['id'])
        obj.cls = PlayableClass.objects.get(class_id=char_data['character_class']['id'])
        obj.level = char_data['level']
        obj.created = datetime.utcfromtimestamp(char_data['last_login_timestamp'] / 1000)
        obj.gender = Gender.objects.get(slug=char_data['gender']['type'])
        obj.current_spec = Spec.objects.get(spec_id=char_data['active_spec']['id'])
        obj.avatar = images['avatar']
        obj.inset = images['inset']
        obj.main = images['main']
        obj.raw = images['raw']

        super().save_model(request, obj, form, change)


admin.site.register(Gender)
admin.site.register(GenderName)
admin.site.register(Faction)
admin.site.register(FactionName)
admin.site.register(PlayableClass)
admin.site.register(ClassName)
admin.site.register(Spec)
admin.site.register(SpecName)
admin.site.register(Race)
admin.site.register(RaceName)
admin.site.register(Realm)
admin.site.register(RealmName)


admin.site.register(GuildRank)
admin.site.register(Guild)
