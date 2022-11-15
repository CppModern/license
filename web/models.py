import random

from django.db import models
from django.utils import timezone as tz
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.
USER = get_user_model()


def gen_license():
    while True:
        key = random.randint(100000, 999999)
        try:
            _ = License.objects.get(key=key)
        except Exception:
            return str(key)


def expiry():
    return tz.now() + tz.timedelta(days=365)


class License(models.Model):
    key = models.CharField(
        "licenss key", max_length=6, editable=False, default=gen_license
    )
    date_created = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(default=expiry)
    created_by = models.ForeignKey(
        USER, related_name="licenses", on_delete=models.CASCADE
    )
    used = models.BooleanField(default=False, blank=True, editable=False)
    mac = models.CharField(max_length=150, blank=True, editable=False)

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = "License"
        verbose_name_plural = "Licenses"
        ordering = ("-expiry_date",)

    def clean(self):
        if not self.key:
            raise ValidationError(_("Key cannot be Empty"))
        if len(self.key) != 6:
            raise ValidationError(_("Key must be six digits"))

    def isExpired(self):
        return tz.now() > self.expiry_date


class Contact(models.Model):
    url = models.URLField(max_length=100)
    key_info = models.CharField(max_length=1000, blank=True)
    key_help_link = models.URLField(max_length=200, blank=True)


class Messagebox(models.Model):
    text = models.TextField(max_length=10000)


class Proxy(models.Model):
    host = models.CharField("Host", max_length=100)
    port = models.IntegerField("Port")
    username = models.CharField("Username", max_length=100)
    password = models.CharField("Password", max_length=100)
