from django.contrib import admin
from workflow import models
from django.contrib.auth.models import User, Group


@admin.register(models.Net)
class Net(admin.ModelAdmin):
    list_display = (
        'name',
        'description'
    )

@admin.register(models.Transition)
class Transition(admin.ModelAdmin):
    list_display = (
        "name",
        "transition_class",
    )

@admin.register(models.Token)
class Token(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'color',
        'location'
    )

@admin.register(models.Location)
class Location(admin.ModelAdmin):
    list_display = (
        "name",
        "description"
    )

@admin.register(models.Arc)
class Arc(admin.ModelAdmin):
    list_display = (
        "type",
        "transition",
        "location"
    )

@admin.register(models.Case)
class Case(admin.ModelAdmin):
    list_display = (
        "id",
        "net",
        "messages"
    )

@admin.register(models.Message)
class Message(admin.ModelAdmin):
    list_display = ("id", )
