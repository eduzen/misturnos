# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from . import managers


class Profile(models.Model):
    # Relations
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="profile",
        verbose_name=_("user")
        )
    # Attributes - Mandatory
    interaction = models.PositiveIntegerField(
        default=0,
        verbose_name=_("interaction")
        )
    # Attributes - Optional
    # Object Manager
    objects = managers.ProfileManager()

    # Custom Properties
    @property
    def username(self):
        return self.user.username

    # Methods

    # Meta and String
    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        ordering = ("user",)

    def __str__(self):
        return u'<%s>' % self.user.username
