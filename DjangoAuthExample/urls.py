"""DjangoAuthExample URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path
import account.views
from authn.views import login_discord
from registration.views import RegisterView
from website.views import home, about

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # Website app
    url(r'^$', home, name='home'),
    url(r'^about/', about, name='about'),

    # Account
    url(r'^account/', account.views.view, name='account_view'),

    # Auth
    url(r'^login/discord', login_discord, name='login_discord'),
    url(r'^login/', LoginView.as_view(template_name='authn/login.html'), name='login', ),
    url(r'^logout/', LogoutView.as_view(template_name='authn/logged_out.html'), name='logout'),
    url('^password_change/done/', PasswordChangeDoneView.as_view(template_name='authn/password_change_done.html'),
        name='password_change_done'),
    url('^password_change/', PasswordChangeView.as_view(template_name='authn/password_change_form.html'),
        name='password_change'),
    url('^password_reset/done/', PasswordResetDoneView.as_view(template_name='authn/password_reset_done.html'),
        name='password_reset_done'),
    url('^password_reset/', PasswordResetView.as_view(template_name='authn/password_reset_form.html'),
        name='password_reset'),
    url('^reset/done/', PasswordResetCompleteView.as_view(template_name='authn/password_reset_complete.html'), name='password_reset_complete'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='authn/password_reset_confirm.html'),
         name='password_reset_confirm'),

    # TODO Registration (with non-enumerable responses and rate limited emails)
    url('^register/', RegisterView.as_view(), name='register'),

    # Social OAuth with Discord
    # Email verification (with rate limited re-sends)
    # /email-verify?token=zzzzzzzz

]
