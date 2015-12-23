# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import post_save
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from . import managers
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class register(View):
    def post(self, request, *args, **kwargs):
        print "\n edu"
        print request.POST['username']
        print request.POST['password']

        user = auth.authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is not None:
            if user.is_active:
                auth.login(request, user)
            else:
                messages.error(request, 'Account not available.')
        else:
            messages.error(
                request,
                'Password incorrect or account not available.'
            )
        return HttpResponseRedirect('/misturnos')

    def get(request, *args, **kwargs):
        print "\ get de login"
        # we should never get to this codepath
        return render(request, 'taskmanager/login.html')


class Profile(models.Model):
    # Relations
    user = models.OneToOneField(
        User,
        related_name="profile",
        verbose_name=_("user"),
        on_delete=models.CASCADE
        )
    # Attributes - Mandatory

    # Attributes - Optional
    # Object Manager

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
    color = models.CharField(
        max_length=7,
        default="#fff",
        validators=[RegexValidator(
            "(^#[0-9a-fA-F]{3}$)|(^#[0-9a-fA-F]{6}$)")],
        verbose_name=_("color"),
        help_text=_("Enter the hex color code, like #ccc or #cccccc")
        )
    # Attributes - Optional
    # Object Manager
    objects = managers.ProjectManager()
    # Custom Properties
    # Methods

    # Meta and String
    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ("user", "name")
        unique_together = ("user", "name")

    def __str__(self):
        return "%s - %s" % (self.user, self.name)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()
