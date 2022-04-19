from authlib.integrations.requests_client import OAuth2Session
from requests.exceptions import HTTPError, Timeout
from django.conf import settings
from time import sleep

from battlenet_client.utils import auth_host
from battlenet_client.wow import profile, game_data
from apps.users import models as user_models
from apps.core import models as core_models
from apps.core.tasks import spec_update, class_update, race_update


credential_client = OAuth2Session(settings.CLIENT_ID, settings.CLIENT_SECRET)
credential_client.fetch_token(f"{auth_host(settings.REGION)}/oauth/token", grant_type='client_credentials')

for region in (('us', 'North America'), ('kr', 'Korea'), ('eu', 'Europe'), ('tw', 'Taiwan'), ('cn', 'China')):
    if region[0] == settings.REGION.lower():
        user_models.Region.objects.update_or_create(tag=region[0], name=region[1], is_active=True)
    else:
        user_models.Region.objects.update_or_create(tag=region[0], name=region[1], is_active=False)

for locale in (('us', 'en', 'US', True), ('us', 'es', 'MX', True), ('us', 'pt', 'BR', True), ('eu', 'en', 'GB', True),
               ('eu', 'es', 'ES', True), ('eu', 'fr', 'FR', True), ('eu', 'ru', 'RU', True), ('eu', 'de', 'DE', True),
               ('eu', 'pt', 'PT', True), ('eu', 'it', 'IT', True), ('kr', 'ko', 'KR', True), ('tw', 'zh', 'TW', True),
               ('cn', 'zh', 'CN', True)):
    db_region = user_models.Region.objects.get(tag=locale[0])
    user_models.Locale.objects.update_or_create(region=db_region, language=locale[1], country=locale[2],
                                                is_active=db_region.is_active)

for gender in (('MALE', 0, 'Bugrom', 'Cenarius'), ('FEMALE', 1, 'Gahdania', 'Zul\'jin')):
    db_gender, _ = core_models.Gender.objects.update_or_create(slug=gender[0], gender_id=gender[1])

    url, params = profile.profile(settings.REGION.lower(), gender[3], gender[2])
    char_data = {}
    retries = 0
    while retries < 5:
        try:
            response = credential_client.get(url, params=params)
            response.raise_for_status()
        except HTTPError as error:
            if error.response.status_code == 429:
                sleep(1)
                continue
        else:
            char_data = response.json()
            break

        retries += 1

    for locale, value in char_data['gender']['name'].items():
        core_models.GenderName.objects.update_or_create(
            locale=user_models.Locale.objects.get(language__iexact=locale[:2], country__iexact=locale[-2:]),
            gender=db_gender,
            name=value)


for faction, realm, char in (('ALLIANCE', 'durotan', 'gahdania'), ('HORDE', 'zuljin', 'gahdania'),
                             ('NEUTRAL', 'zuljin', 'gahdsie')):
    db_faction, _ = core_models.Faction.objects.update_or_create(slug=faction)
    retries = 0
    url, params = profile.profile(settings.REGION, realm, char)
    while retries < 5:
        try:
            response = credential_client.get(url, params=params)
            response.raise_for_status()
        except HTTPError as error:
            if error.response.status_code == 429:
                sleep(1)
                retries += 1
                continue
        except Timeout:
            retries += 1
        else:
            char_data = response.json()
            break

    for locale in char_data['faction']['name'].keys():
        core_models.FactionName.objects.update_or_create(
            locale=user_models.Locale.objects.get(language__iexact=locale[:2], country__iexact=locale[-2:]),
            faction=db_faction,
            name=char_data['faction']['name'][locale])


db_region = core_models.Region.objects.get(tag__iexact=settings.Region)

class_update()

spec_update()

race_update()
