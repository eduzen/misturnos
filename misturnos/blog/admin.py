# -*- coding: utf-8 -*-
from django.contrib import admin
from . import models

admin.site.register(models.Post)
# admin.site.register(models.Address)


class AddressInLine(admin.TabularInline):
    model = models.Address
    extra = 0


class ProjectsInLine(admin.TabularInline):
    model = models.Project
    extra = 0


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("username", "_projects")
    search_fields = ["user__username"]
    inlines = [
       AddressInLine,
       ProjectsInLine
    ]

    def _projects(self, obj):
        return obj.projects.all().count()
