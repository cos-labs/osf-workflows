from django.contrib import admin
from workflow import models
from django.contrib.auth.models import User, Group

@admin.register(models.Workflow)
class Workflow(admin.ModelAdmin):
    pass

@admin.register(models.Operation)
class Operation(admin.ModelAdmin):
    list_display = ("name", "operation", "return_value")

@admin.register(models.Parameter)
class Parameters(admin.ModelAdmin):
    list_display = ("id", "name", "value", "operation")

@admin.register(models.Value)
class Value(admin.ModelAdmin):
    list_display = ("name", "description")

@admin.register(models.Context)
class Context(admin.ModelAdmin):
    list_display = ("id", )

@admin.register(models.Message)
class Message(admin.ModelAdmin):
    list_display = ("id", )

@admin.register(models.Service)
class Service(admin.ModelAdmin):
    pass

@admin.register(models.Resource)
class Resource(admin.ModelAdmin):
    pass

@admin.register(models.Role)
class Role(admin.ModelAdmin):
    list_display = ("name", "responsibilities")
