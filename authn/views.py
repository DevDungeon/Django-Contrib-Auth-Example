from django.http import HttpResponseRedirect
from DjangoAuthExample import settings


def login_discord(request):
    return HttpResponseRedirect(settings.DISCORD_SOCIAL_LOGIN_URL)
