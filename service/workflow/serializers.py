# -*- coding: utf-8 -*-
"""Workflow Serializers"""


from rest_framework.serializers import CharField
from rest_framework_json_api import serializers, relations
from django.contrib.auth.models import User, Group

from workflow import models


class Workflow(serializers.ModelSerializer):

    class Meta:
        model = models.Workflow
        fields = (
            'id',
            'name',
            'description',
            'group',
            'resolver',
            'ctxs'
        )

    class JSONAPIMeta:
        resource_name = 'workflows'


class Operation(serializers.ModelSerializer):

    name = CharField(max_length=64, required=False)
    operation = CharField(max_length=32, required=False)
    group = relations.ResourceRelatedField(
        queryset=Group.objects.all()
    )
    args = relations.ResourceRelatedField(
        many=True,
        queryset=models.Value.objects.all()
    )

    class Meta:
        model = models.Operation
        fields = (
            'id',
            'name',
            'description',
            'group',
            'operation',
            'args',
            'parameters',
            'return_value',
            'view',
            'messages',
            'caller'
        )

    class JSONAPIMeta:
        resource_name = 'operations'


class Value(serializers.ModelSerializer):

    source_operation = relations.ResourceRelatedField(
        required=False,
        queryset=models.Operation.objects.all()
    )

    class Meta:
        model = models.Value
        fields = (
            'key',
            'name',
            'description',
            'type',
            'operations',
            'source_operation'
        )

    class JSONAPIMeta:
        resoure_name = 'values'


class Context(serializers.ModelSerializer):

    messages = relations.ResourceRelatedField(
        required=False,
        many=True,
        queryset=models.Message.objects.all()
    )
    heirs = relations.ResourceRelatedField(
        required=False,
        many=True,
        queryset=models.Context.objects.all()
    )

    class Meta:
        model = models.Context
        fields = (
            'id',
            'values',
            'inherit',
            'heirs',
            'workflows',
            'messages'
        )


class Message(serializers.ModelSerializer):
    
    class Meta:
        model = models.Message
        fields = (
            'id',
            'message_type',
            'timestamp',
            'origin',
            'response',
            'ctx',
            'content',
        )

    class JSONAPIMeta:
        resource_name = 'messages'


class Role(serializers.ModelSerializer):

    class Meta:
        model = models.Role
        fields = (
            'name',
            'responsibilities',
            'operation'
        )

    class JSONAPIMeta:
        resource_name = 'roles'


class Service(serializers.ModelSerializer):

    class Meta:
        model = models.Service
        fields = (
            'name',
            'description',
            'base_url',
        )

    class JSONAPIMeta:
        resource_name = 'services'


class Resource(serializers.ModelSerializer):

    class Meta:
        model = models.Resource
        fields = (
            'name',
            'description',
            'service'
        )

    class JSONAPIMeta:
        resource_name = 'resources'


class User(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
        )

    class JSONAPIMeta:
        resource_name = 'users'

class Group(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = (
            'name',
        )
