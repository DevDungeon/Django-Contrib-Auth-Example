from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.forms import Form, CharField, EmailField, PasswordInput
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import FormView
from DjangoAuthExample import settings


@login_required
def profile(request):
    print(request.user)
    print(request.user.get_username())
    print(request.user.get_full_name())
    print(request.user.get_short_name())
    return HttpResponse("Welcome to your private profile! %s <a href=\"/logout\">Logout</a>" % request.user)


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
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        except IntegrityError as e:
            print("Error when registering a new user: %s" % e)
            return HttpResponse('Thank you for registering, an email has been sent.')


def register_new_user(form, request):
    existing_user = User.objects.filter(email=form.cleaned_data['email'])

    if existing_user.exists():
        # TODO put email sub/body in template w/ i18n translation
        # TODO rate limit email
        existing_user.first().email_user('Attempted registration on __site___',
                                 'Hello, someone attempted to register your email address at ______ but you are already registered. If you forgot your password, visit this forgot password page')
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
