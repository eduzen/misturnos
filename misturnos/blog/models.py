from __future__ import unicode_literals
# -*- coding: utf-8 -*-
import os
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


def get_image_path(instance, filename):
    return os.path.join('users', str(instance.id), filename)


class Post(models.Model):
    # Relations
    author = models.ForeignKey(User)
    # Attributes
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    # Methods
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __unicode__(self):
        return self.title


class Profile(models.Model):
    # Relations
    user = models.OneToOneField(
        User,
        related_name="profile",
        verbose_name=_("user"),
        on_delete=models.CASCADE
        )
    # Attributes
    profession = models.CharField(max_length=100)
    phone_regex = RegexValidator(
        regex=r'^\d{8,13}$',
        message="Phone number must be entered in the format: '99999999'."
        "Up to 13 digits allowed."
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=13,
        blank=True
    )
    avatar = models.ImageField(
        upload_to=get_image_path,
        blank=True,
        null=True
    )

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

    def __unicode__(self):
        return u'<%s>' % self.user.username


class Address(models.Model):
    # Relations
    profile = models.ForeignKey(Profile)

    # Attributes
    address_type = models.CharField(
        max_length=10,
    )
    address = models.CharField(
        max_length=255,
    )
    city = models.CharField(
        max_length=255,
    )
    state = models.CharField(
        max_length=2,
    )
    postal_code = models.CharField(
        max_length=20,
    )

    class Meta:
        unique_together = ('profile', 'address_type',)


class Project(models.Model):
    # Relations
    user = models.ForeignKey(
        Profile,
        related_name="projects",
        verbose_name=_("user")
        )
    # Attributes - Mandatory
    name = models.CharField(
        max_length=100,
        verbose_name=_("name"),
        help_text=_("Ingrese el nombre del proyecto")
        )
    # Attributes - Optional

    # Methods

    # Meta and String
    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ("user", "name")
        unique_together = ("user", "name")

    def __unicode__(self):
        return "%s - %s" % (self.user, self.name)


@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()
