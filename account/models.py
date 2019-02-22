from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey, IntegerField


class Account(models.Model):
    user = ForeignKey(User, on_delete=models.DO_NOTHING)
    # tokens = IntegerField()
