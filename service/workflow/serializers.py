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
            'resolver'
        )

    class JSONAPIMeta:
        resource_name = 'workflows'


class Operation(serializers.ModelSerializer):

    name = CharField(max_length=64, required=False)
    operation = CharField(max_length=32, required=False)
    group = relations.ResourceRelatedField(
        queryset=Group.objects.all()
    )
    parameters = relations.ResourceRelatedField(
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
            'parameters',
            'view',
        )

    class JSONAPIMeta:
        resource_name = 'operations'


class Value(serializers.ModelSerializer):

    class Meta:
        model = models.Value
        fields = (
            'id',
            'name',
            'description',
            'type',
            'value',
            'operations',
            'contexts',
        )

    class JSONAPIMeta:
        resoure_name = 'values'


class Context(serializers.ModelSerializer):

    values = relations.ResourceRelatedField(
        required=False,
        many=True,
        queryset=models.Value.objects.all()
    )

    class Meta:
        model = models.Context
        fields = (
            'id',
            'values',
            'messages'
        )


class Message(serializers.ModelSerializer):

    class Meta:
        model = models.Message
        fields = (
            'id',
            'message_type',
            'timestamp',
            'workflow',
            'origin',
            'response',
            'context',
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
