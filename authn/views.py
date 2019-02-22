from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.forms import Form, CharField, EmailField, PasswordInput
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse
from django.views.generic import FormView
from DjangoAuthExample import settings



class RegisterForm(Form):
    username = CharField()
    first_name = CharField()
    last_name = CharField()
    email = EmailField()
    password = CharField(widget=PasswordInput)
    password_confirm = CharField(widget=PasswordInput)

    def clean_password_confirm(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password_confirm'):
            raise ValidationError('Password fields do not match.')


class RegisterView(FormView):
    template_name = 'authn/register.html'
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):

        try:
            register_new_user(form, self.request)
            messages.success(self.request, 'Thank you for registering. You have been automatically logged in.')
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        except IntegrityError as e:
            print("Error when registering a new user: %s" % e)
            return HttpResponse(get_template('authn/registration_complete.html').render())


def register_new_user(form, request):
    existing_user = User.objects.filter(email=form.cleaned_data['email'])

    if existing_user.exists():
        # TODO put email sub/body in template w/ i18n translation
        # TODO rate limit email
        password_reset_url = request.scheme + '://' + request.get_host() + reverse('password_reset')
        existing_user.first().email_user(get_template('emails/already_registered_subject.txt').render(context={'site_name': settings.SITE_NAME}),
                                         get_template('emails/already_registered.html').render(context={'password_reset_url': password_reset_url}))
        raise IntegrityError("Email already exists: %s" % form.cleaned_data['email'])
    else:
        # Create and log in user
        newly_created_user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'])
        login(request, newly_created_user)
        # TODO send rate limited email verification


def login_discord(request):
    return HttpResponseRedirect(settings.DISCORD_SOCIAL_LOGIN_URL)


"""
API_ENDPOINT = 'https://discordapp.com/api/v6'
CLIENT_ID = '332269999912132097'
CLIENT_SECRET = '937it3ow87i4ery69876wqire'
REDIRECT_URI = 'https://nicememe.website'

def exchange_code(code):
  data = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': REDIRECT_URI,
    'scope': 'identify email connections'
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  r = requests.post('%s/oauth2/token' % API_ENDPOINT, data, headers)
  r.raise_for_status()
  return r.json()
"""
