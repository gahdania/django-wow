from __future__ import absolute_import, unicode_literals

from datetime import datetime

import pytz
from os.path import basename
from io import BytesIO
from authlib.integrations.requests_client import OAuth2Session
from requests.exceptions import HTTPError, Timeout
from django.conf import settings
from time import sleep

from battlenet_client.utils import auth_host, slugify
from battlenet_client.wow import profile, game_data
from django_wow.celery import app
from apps.users.models import Account, Locale
from . import models

credential_client = OAuth2Session(settings.CLIENT_ID, settings.CLIENT_SECRET)
credential_client.fetch_token(f"{auth_host(settings.REGION)}/oauth/token", grant_type='client_credentials')


def get_media(char_data: dict, params) -> dict:

    images = {}
    media_data = {}

    gender = 1 if char_data['gender']['type'] == 'FEMALE' else 0

    try:
        retries = 0
        while retries < 5:
            try:
                response = credential_client.get(char_data['media']['href'], params=params)
                response.raise_for_status()
            except HTTPError as error:
                if error.response.status_code == 429:
                    sleep(1)
                    retries += 1
                    continue
                else:
                    break
            else:
                media_data = response.json()
                break

        if 'assets' in media_data:
            for asset in media_data['assets']:

                url_string = f"{asset['value']}?alt=/shadow/avatar/{char_data['race']['id']}-{gender}.jpg"
                if asset['key'].endswith('raw'):
                    images['raw'] = url_string
                else:
                    images[asset['key']] = url_string
        else:
            images['avatar'] = f"{media_data['avatar_url']}?alt=/shadow/avatar/{char_data['race']['id']}-{gender}.jpg"
            images['inset'] = f"{media_data['bust_url']}?alt=/shadow/avatar/{char_data['race']['id']}-{gender}.jpg"
            images['main'] = f"{media_data['render_url']}?alt=/shadow/avatar/{char_data['race']['id']}-{gender}.jpg"
            images['raw'] = ''
    except KeyError as error:
        print(f"{error}: {char_data['name']} - {char_data['realm']['slug']}")

    return images


@app.task
def process_characters(wow_accounts):
    completed = 0

    for account_idx in wow_accounts:
        for char_idx in account_idx['characters']:
            if process_character(account_idx['id'], char_idx['realm']['slug'], char_idx['name']):
                completed += 1

    return f"Characters Updated/Added: {completed}"


@app.task
def process_character(account, realm_slug, character):

    char_data = {}
    account = Account.objects.get(account_number=account)
    realm = models.Realm.objects.get(region=account.user.region, slug__iexact=realm_slug)
    url, params = profile.profile(account.user.region.tag, realm_slug, character, status=True,
                                  locale=account.user.preferred_locale.__str__())
    print(f"Processing: {character} - {realm_slug.title()}")
    try:
        db_char = models.Character.objects.get(account=account, realm__slug__iexact=realm_slug,
                                               name__iexact=character)
    except models.Character.DoesNotExist:
        # character des not exist in the database

        url, params = profile.profile(account.user.region.tag, realm_slug, character,
                                      locale=account.user.preferred_locale.__str__())
        for _ in range(5):
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
    else:
        status = None

        for _ in range(5):
            try:
                response = credential_client.get(url, params=params)
                response.raise_for_status()
            except HTTPError as error:
                if error.response.status_code == 429:
                    sleep(1)
                    continue
                if error.response.status_code == 404:
                    db_char.delete()
                    status = None
                    break
            else:
                status = response.json()

        if 'is_valid' in status and not status['is_valid']:
            db_char.delete()

        if character.character_id != status['id']:
            db_char.delete()

        url, params = profile.profile(account.user.region.tag, realm_slug, character,
                                      locale=account.user.preferred_locale.__str__())
        for _ in range(5):
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
    finally:
        if char_data:
            images = get_media(char_data, params)

            gender = models.Gender.objects.get(slug=char_data['gender']['type'])
            race = models.Race.objects.get(race_id=char_data['race']['id'])
            spec = None
            db_char = None

            try:
                spec = models.Spec.objects.get(spec_id=char_data['active_spec']['id'])
            except KeyError as error:
                if error == 'active_spec':
                    spec = None

            try:
                print(f"Creating: {char_data['name']} {char_data['realm']['slug']}")
                db_char, created = models.Character.objects.update_or_create(
                    account=account,
                    character_id=char_data['id'],
                    name=char_data['name'],
                    realm=realm,
                    race=race,
                    gender=gender,
                    level=char_data['level'],
                    cls=models.PlayableClass.objects.get(class_id=char_data['character_class']['id']),
                    last_updated=datetime.fromtimestamp(char_data['last_login_timestamp'] / 1000, pytz.UTC),
                    current_spec=spec,
                    avatar=images['avatar'],
                    inset=images['inset'],
                    main=images['main'],
                    raw=images['raw'],
                    created=None)
            except KeyError as error:
                print(f"{error}: {char_data['name']} - {char_data['realm']['slug']}")
            else:
                db_char.save()

            if db_char:
                return True

            return False

        return False


@app.task
def class_update():

    class_list = []

    url, params = game_data.playable_class(settings.REGION)
    for _ in range(5):
        try:
            response = credential_client.get(url, params=params)
            response.raise_for_status()
        except HTTPError as error:
            if error.response.status_code == 429:
                sleep(1)
                continue
        else:
            class_list = response.json()['class']
            break

    for class_idx in class_list:
        class_data = {}
        media_data = {}
        image_data = None
        for _ in range(5):
            try:
                response = credential_client.get(class_idx['key']['href'], params=params)
                response.raise_for_status()
            except HTTPError as error:
                if error.response.status_code == 429:
                    sleep(1)
                    continue
            else:
                class_data = response.json()
                break

        if class_data:
            print(f"Updating: {class_data['name']['en_US']}")
            for _ in range(5):
                try:
                    response = credential_client.get(class_data['media']['key']['href'], params=params)
                    response.raise_for_status()
                except HTTPError as error:
                    if error.response.status_code == 429:
                        sleep(1)
                        continue
                else:
                    media_data = response.json()
                    break

            if media_data:
                for _ in range(5):
                    try:
                        response = credential_client.get(media_data['assets'][0]['value'], params=params)
                        response.raise_for_status()
                    except HTTPError as error:
                        if error.response.status_code == 429:
                            sleep(1)
                            continue
                    else:
                        image_data = BytesIO(response.content)
                        break

            try:
                db_cls, created = models.PlayableClass.objects.update_or_create(
                    class_id=class_data['id'],
                    slug=class_data['name']['en_US'].lower()
                )

            except TypeError as error:
                print(error)
            else:
                if not created:
                    db_cls.icon.delete()

                db_cls.icon.save(basename(media_data['assets'][0]['value']), image_data)

                for locale in class_data['name'].keys():
                    db_locale = Locale.objects.get(language__iexact=locale[:2], country__iexact=locale[-2:])
                    models.ClassName.objects.update_or_create(locale=db_locale, cls=db_cls,
                                                              name=class_data['name'][locale],
                                                              male=class_data['gender_name']['male'][locale],
                                                              female=class_data['gender_name']['female'][locale])


@app.task
def spec_update():

    spec_list = []

    url, params = game_data.playable_spec(settings.REGION)
    for _ in range(5):
        try:
            response = credential_client.get(url, params=params)
            response.raise_for_status()
        except HTTPError as error:
            if error.response.status_code == 429:
                sleep(1)
                continue
        else:
            spec_list = response.json()['character_specializations']
            break

    for spec_idx in spec_list:
        spec_data = {}
        media_data = {}
        image_data = None
        for _ in range(5):
            try:
                response = credential_client.get(spec_idx['key']['href'], params=params)
                response.raise_for_status()
            except HTTPError as error:
                if error.response.status_code == 429:
                    sleep(1)
                    continue
            else:
                spec_data = response.json()
                break

        if spec_data:
            print(f"Updating: {spec_data['name']['en_US']}")
            for _ in range(5):
                try:
                    response = credential_client.get(spec_data['media']['key']['href'], params=params)
                    response.raise_for_status()
                except HTTPError as error:
                    if error.response.status_code == 429:
                        sleep(1)
                        continue
                else:
                    media_data = response.json()
                    break

            if media_data:
                for _ in range(5):
                    try:
                        response = credential_client.get(media_data['assets'][0]['value'], params=params)
                        response.raise_for_status()
                    except HTTPError as error:
                        if error.response.status_code == 429:
                            sleep(1)
                            continue
                    else:
                        image_data = BytesIO(response.content)
                        break

            try:
                db_cls = models.PlayableClass.objects.get(pk=spec_data['playable_class']['id'])
                db_spec, created = models.Spec.objects.update_or_create(
                    spec_id=spec_data['id'],
                    slug=spec_data['name']['en_US'].lower(),
                    cls=db_cls
                )

            except TypeError as error:
                print(error)
            else:
                if not created:
                    db_spec.icon.delete()

                db_spec.icon.save(basename(media_data['assets'][0]['value']), image_data)

                for locale in spec_data['name'].keys():
                    db_locale = Locale.objects.get(language__iexact=locale[:2], country__iexact=locale[-2:])
                    models.SpecName.objects.update_or_create(locale=db_locale, spec=db_spec,
                                                             name=spec_data['name'][locale],
                                                             male=spec_data['gender_description']['male'][locale],
                                                             female=spec_data['gender_description']['female'][locale])


@app.task
def race_update():
    retries = 0
    race_list = []
    race_data = {}
    url, params = game_data.playable_race(settings.REGION.lower())
    while retries < 5:
        try:
            response = credential_client.get(url, params=params)
            response.raise_for_status()
        except HTTPError as error:
            if error.response.status_code == 429:
                sleep(1)
                continue
        except Timeout:
            retries += 1

        else:
            race_list = response.json()['races']
            break

    if race_list:
        for race_idx in race_list:
            while retries < 5:
                try:
                    response = credential_client.get(race_idx['key']['href'], params=params)
                    response.raise_for_status()
                except HTTPError as error:
                    if error.response.status_code == 429:
                        sleep(1)
                        continue
                except Timeout:
                    retries += 1
                else:
                    race_data = response.json()
                    break
            db_race, _ = models.Race.objects.update_or_create(
                slug=slugify(race_data['name']['en_US']),
                race_id=race_data['id'],
                faction=models.Faction.objects.get(slug__iexact=race_data['faction']['type'])
            )

            for locale in race_data['name'].keys():
                models.RaceName.objects.update_or_create(
                    race=db_race,
                    locale=models.Locale.objects.get(language__iexact=locale[:2], country__iexact=locale[-2:]),
                    name=race_data['name'][locale],
                    male=race_data['gender_name']['male'][locale],
                    female=race_data['gender_name']['male'][locale])


@app.task
def connected_realm_update():
    retries = 0
    cr_list = []
    cr_data = {}
    db_regions = models.Region.objects.filter(is_active=True)

    for db_region in db_regions:
        url, params = game_data.connected_realm(db_region.tag)
        while retries < 5 or not cr_list:
            try:
                response = credential_client.get(url, params=params)
                response.raise_for_status()
            except HTTPError as error:
                if error.response.status_code == 429:
                    sleep(1)
                    retries += 1
                    continue
            else:
                cr_list = response.json()['connected_realms']
                break

        for cr_idx in cr_list:
            retries = 0
            while retries < 5 or not cr_data:
                try:
                    response = credential_client.get(cr_idx['href'])
                    response.raise_for_status()
                except HTTPError as error:
                    if error.response.status_code == 429:
                        retries += 1
                        sleep(1)
                except Timeout:
                    retries += 1
                else:
                    cr_data = response.json()
                    break
            db_cr, created = models.ConnectedRealm.objects.update_or_create(
                connected_realm_id=cr_data['id']
            )

            for realm in cr_data['realms']:
                db_realm, created = models.Realm.objects.update_or_create(
                    slug=realm['slug'],
                    realm_id=realm['id'],
                    region=db_region,
                    type=models.RealmType.objects.get(slug=realm['type']['type']),
                    timezone=realm['timezone'],
                    is_tournament_realm=realm['is_tournament']
                )
                db_cr.connected_realms.add(db_realm)
                for locale, value in realm['name'].items():
                    models.RealmName.objects.update_or_create(
                        realm=db_realm,
                        locale=models.Locale.objects.get(language__iexact=locale[:2], country__iexact=locale[-2:]),
                        name=value
                    )


@app.task
def realm_type_update(tests):
    for realm_type, realm_name in tests:
        db_realm_type, _ = models.RealmType.objects.update_or_create(
            slug=realm_type
        )

        url, params = game_data.realm(settings.REGION, realm_slug=realm_name)
        retries = 0
        realm_data = {}
        while retries < 5 or not realm_data:

            try:
                response = credential_client.get(url, params=params)
                response.raise_for_status()
            except HTTPError as error:
                if error.response.status_code == 429:
                    retries += 1
                    sleep(1)
            except Timeout:
                retries += 1
            else:
                realm_data = response.json()
                break

        for locale, value in realm_data['type']['name'].items():
            models.RealmTypeName.objects.update_or_create(
                realm_type=db_realm_type,
                locale=models.Locale.objects.get(language__iexact=locale[:2], country__iexact=locale[-2:]),
                name=value
            )

