from django.contrib import admin
from workflow import models
from django.contrib.auth.models import User, Group

@admin.register(models.Workflow)
class Workflow(admin.ModelAdmin):
    pass

@admin.register(models.Operation)
class Operation(admin.ModelAdmin):
    pass

@admin.register(models.Argument)
class Argument(admin.ModelAdmin):
    pass

@admin.register(models.Value)
class Value(admin.ModelAdmin):
    pass

@admin.register(models.Context)
class Context(admin.ModelAdmin):
    pass

@admin.register(models.Message)
class Message(admin.ModelAdmin):
    pass

@admin.register(models.Service)
class Service(admin.ModelAdmin):
    pass

@admin.register(models.Resource)
class Resource(admin.ModelAdmin):
    pass

@admin.register(models.Role)
class Role(admin.ModelAdmin):
    pass
