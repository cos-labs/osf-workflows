# -*- coding: utf-8 -*-
"""Workflow Models"""


from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User, Group

import uuid

from workflow.utils import camelCase


class Workflow(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    description = models.TextField()
    group = models.ForeignKey('auth.Group', default=1)
    resolver = models.ForeignKey('Operation')


class Operation(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    description = models.TextField()
    group = models.ForeignKey('auth.Group', default=1)
    operation = models.CharField(max_length=32) # Needs a manifest in the module so they can't call builtins
    parameters = models.ManyToManyField(
        'Value',
        related_name='operations',
        blank=True
    )
    view = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Value(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=24)
    description = models.TextField()
    type = models.TextField(default='Any')
    value = models.TextField()

    def __str__():
        return self.name


class Context(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    values = models.ManyToManyField('Value', related_name='contexts')


class Message(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    message_type = models.CharField(max_length=24)
    timestamp = models.DateTimeField(auto_now_add=True)
    context = models.ForeignKey('Context', related_name='messages')
    origin = models.ManyToManyField(
        'Operation',
        related_name='messages',
        default=None
    )
    response = models.ForeignKey(
        'Operation',
        related_name='caller',
        default=None
    )
    content = models.TextField()


class Service(models.Model):

    name = models.CharField(max_length=24)
    description = models.TextField()
    base_url = models.TextField()

    def __str__(self):
        return self.name


class Resource(models.Model):

    name = models.CharField(max_length=24)
    description = models.TextField()
    service = models.ManyToManyField('Service')


class Role(models.Model):

    name = models.CharField(max_length=24)
    responsibilities = models.TextField()
    operation = models.ForeignKey(
        'Operation',
        related_name='roles',
        default=None,
        blank=True,
    )

    def __str__(self):
        return self.name

