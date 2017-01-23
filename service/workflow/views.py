# -*- coding: utf-8 -*-
"""Workflow Views"""



from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework_json_api.views import RelationshipView
from rest_framework.exceptions import APIException

import json

from workflow import models
from workflow import serializers
from workflow import operations
from workflow import utils


class Workflow(viewsets.ModelViewSet):
    queryset = models.Workflow.objects.all()
    serializer_class = serializers.Workflow


class Operation(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace', 'run']
    queryset = models.Operation.objects.all()
    serializer_class = serializers.Operation

    def run(self, request, *args, **kwargs):

        user_parameters = json.loads(request.body)
        context = models.Context.objects.get(pk=user_parameters.pop('ctx', None))
        if not context:
            return Response({
                "status": "404",
                "title": "context does not exist",
                "description": "the requested context does not currently exist"
            }, status=status.http_404_not_found)

        operation = models.Operation.objects.get(pk=kwargs['pk'])
        parameters = {}
        for arg in operation.arguments.all():
            operation_parameter = user_parameters.get(arg.value.key, None)
            if arg.value.type.split(' ')[0] != 'IO':
                operation_parameter = context.values.get(arg.value.key, None)
            if not operation_parameter:
                return Response({
                    "status": "404",
                    "title": "Missing Parameter",
                    "description": "<Paramter: {}> is missing.".format(arg.value.key)
                }, status=status.HTTP_404_NOT_FOUND)
            parameters[arg.name] = operation_parameter
            context.values[arg.value.key] = operation_parameter

        result = getattr(operations, operation.operation)(**parameters)
        context.values[operation.return_value.key] = result
        context.save()

        new_operations = []
        operations_to_check = models.Operation.objects.filter(parameters__in=[operation.return_value.pk])
        for operation in operations_to_check:
            new_operations.extend(utils.get_allowed_operations(context, operation))

        for operation in new_operations:
            message = models.Message()
            message.message_type = 'Request'
            message.response = operation
            message.content = 'Your input is required to {}.'.format(operation.name)
            message.ctx = context
            message.save()

        return Response("Success")

    def get_queryset(self):
        queryset=self.queryset
        #if 'operation_pk' in self.kwargs:
        #    import ipdb; ipdb.set_trace()
        #    queryset = queryset.filter(prerequisites=None)
        #    return queryset
        #if 'prerequisites' in self.request.query_params:
        #    queryset = queryset.filter(prerequisites=None)
        #    return queryset
            #return queryset.filter(prerequisites__pk=self.kwargs['operation_pk'])
        return queryset


class OperationRelationship(RelationshipView):
    queryset = models.Operation.objects.all()
    serializer_class = models.Operation


class Value(viewsets.ModelViewSet):
    queryset = models.Value.objects.all()
    serializer_class = serializers.Value


class Context(viewsets.ModelViewSet):
    queryset = models.Context.objects.all()
    serializer_class = serializers.Context

    def perform_create(self, serializer):

        context = serializer.save()
        context.values = {
            'editor_role': 'Editor',
            'reviewer_role': 'Reviewer',
            'editor_count': 1,
            'reviewer_count': 3
        }
        context.save()

        allowed_operations = []
        for workflow in context.workflows.all():
            resolver = workflow.resolver
            allowed_operations.extend(utils.get_allowed_operations(context, resolver))

        for operation in allowed_operations:
            message = models.Message()
            message.message_type = 'Request'
            message.response = operation
            message.content = 'Your input is required to {}.'.format(operation.name)
            message.ctx = context
            message.save()


class Message(viewsets.ModelViewSet):
    queryset = models.Message.objects.all()
    serializer_class = serializers.Message

    def get_queryset(self):
        queryset = self.queryset
        return queryset


class Service(viewsets.ModelViewSet):
    queryset = models.Service.objects.all()
    serializer_class = serializers.Service


class ServiceRelationship(RelationshipView):
    queryset = models.Service.objects.all()
    serializer_class = serializers.Service


class Resource(viewsets.ModelViewSet):
    queryset = models.Resource.objects.all()
    serializer_class = serializers.Resource


class Role(viewsets.ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = serializers.Role


class User(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.User


class Group(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.Group
