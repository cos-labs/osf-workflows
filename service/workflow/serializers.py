# -*- coding: utf-8 -*-
"""Workflow Serializers"""


from rest_framework.serializers import CharField
from rest_framework_json_api import serializers, relations
from django.contrib.auth.models import User, Group

from workflow import models


class Net(serializers.ModelSerializer):

    class Meta:
        resource_name = 'nets'
        model = models.Net
        fields = (
            'id',
            'name',
            'description',
            'group',
            'cases',
            'transitions',
            'locations',
        )


class Transition(serializers.ModelSerializer):

    name = CharField(max_length=128, required=False)
    transition_class = CharField(max_length=128, required=False)
    group = relations.ResourceRelatedField(
        queryset=Group.objects.all()
    )
    inputs = relations.ResourceRelatedField(
        many=True,
        queryset=models.Location.objects.all()
    )
    outputs = relations.ResourceRelatedField(
        many=True,
        queryset=models.Location.objects.all()
    )

    class Meta:
        resource_name = 'transitions'
        model = models.Transition
        fields = (
            'id',
            'name',
            'description',
            'group',
            'transition_class',
            'inputs',
            'outputs',
            'messages',
            'net',
            'arcs'
        )


class Token(serializers.ModelSerializer):

    location = relations.ResourceRelatedField(
        required=False,
        queryset=models.Location.objects.all()
    )

    net = relations.ResourceRelatedField(
        required=False,
        queryset=models.Net.objects.all()
    )

    case = relations.ResourceRelatedField(
        required=False,
        queryset=models.Case.objects.all()
    )

    request_messages = relations.ResourceRelatedField(
        required=False,
        many=True,
        queryset=models.Message.objects.all()
    )

    class Meta:
        resource_name = 'tokens'
        model = models.Token
        fields = (
            'color',
            'case',
            'location',
            'request_messages',
            'name',
            'net'
        )


class Location(serializers.ModelSerializer):

    sources = relations.ResourceRelatedField(
        many=True,
        queryset=models.Transition.objects.all()
    )
    targets = relations.ResourceRelatedField(
        many=True,
        queryset=models.Transition.objects.all()
    )

    class Meta:
        resource_name = 'locations'
        model = models.Location
        fields = (
            'name',
            'description',
            'type',
            'net',
            'targets',
            'arcs',
            'tokens',
            'sources'
        )


class Arc(serializers.ModelSerializer):

    class Meta:
        resource_name = 'arcs'
        model = models.Arc
        fields = (
            'type',
        )


class Case(serializers.ModelSerializer):

    messages = relations.ResourceRelatedField(
        required=False,
        many=True,
        queryset=models.Message.objects.all()
    )

    class Meta:
        resource_name = 'cases'
        model = models.Case
        fields = (
            'id',
            'net',
            'messages'
        )


class Message(serializers.ModelSerializer):
    
    response_tokens = relations.ResourceRelatedField(
        required=False,
        many=True,
        queryset=models.Token.objects.all()
    )

    class Meta:
        resource_name = 'messages'
        model = models.Message
        fields = (
            'id',
            'message_type',
            'timestamp',
            'origin',
            'response',
            'case',
            'content',
            'view',
            'section',
            'response_tokens',
            'response_token_name'
        )


class User(serializers.ModelSerializer):

    class Meta:
        resource_name = 'users'
        model = User
        fields = (
            'id',
            'username',
        )


class Group(serializers.ModelSerializer):

    class Meta:
        resource_name = 'groups'
        model = Group
        fields = (
            'name',
        )
