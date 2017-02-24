# -*- coding: utf-8 -*-
"""Workflow Models"""


from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User, Group

import uuid

from workflow.utils import camelCase
from workflow import managers


class Workflow(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    description = models.TextField()
    group = models.ForeignKey('auth.Group', default=1)
    resolver = models.ForeignKey('Operation')

    def __str__(self):
        return self.name


class Operation(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    description = models.TextField()
    group = models.ForeignKey('auth.Group', default=1)
    operation = models.CharField(max_length=32) # Needs a manifest in the module so they can't call builtins
    args = models.ManyToManyField(
        'Value',
        related_name='operations',
        through='Parameter',
        blank=True
    )
    return_value = models.OneToOneField('Value', null=True, related_name='source_operation')
    view = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Parameter(models.Model):

    operation = models.ForeignKey('Operation', related_name="parameters")
    value = models.ForeignKey('Value', related_name="parameters")
    name = models.CharField(max_length=32, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.value.key
        super().save(*args, **kwargs)

    def __str__(self):
        return '<Parameters: Operation: {}; {} => {}>'.format(self.operation.name, self.value.key, self.name)


class Value(models.Model):

    key = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=24)
    description = models.TextField()
    type = models.TextField(default='Any')

    def __str__(self):
        return self.name


class Context(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    values = JSONField(default={}, blank=True)
    inherit = models.ForeignKey('Context', related_name='heirs', null=True, blank=True)
    workflows = models.ManyToManyField('Workflow', related_name='ctxs', blank=True)

    def __str__(self):
        return str(self.id.urn)


class Message(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    message_type = models.CharField(max_length=24)
    timestamp = models.DateTimeField(auto_now_add=True)
    ctx = models.ForeignKey('Context', related_name='messages')
    origin = models.ManyToManyField(
        'Operation',
        related_name='messages',
        default=None
    )
    response = models.ForeignKey(
        'Operation',
        related_name='caller',
        default=None,
        null=True
    )
    content = models.TextField()

    def __str__(self):
        return 'Message: {}'.format(self.id.urn)


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

