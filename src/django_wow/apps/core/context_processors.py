from django.conf import settings


def guild_string(request):
    return {'guild_name': f"{settings.GUILD} ({settings.REALM}-{settings.REGION})"}
