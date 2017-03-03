# -*- coding: utf-8 -*-
"""Workflow Views"""



from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework_json_api.views import RelationshipView
from rest_framework.exceptions import APIException

import json
import copy

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

    def run(self, request, *args, **kwargs):

        user_args = json.loads(request.body)
        context = models.Context.objects.get(pk=user_args.pop('ctx', None))
        if not context:
            return Response({
                "status": "404",
                "title": "Context Does Not Exist",
                "description": "The requested context does not currently exist."
            }, status=status.http_404_not_found)

        # TODO Use the following line to run an optimized
        # version of `run` that only runs the affected fns.
        # Onf faliure here, defer to recreating the available messages
        #operation = models.Operation.objects.get(pk=kwargs['pk'])


        previous_context = None
        while not previous_context == context.values: # This is ugly.
            previous_context = copy.deepcopy(context.values)
            # Delete all current messages.
            context.messages.all().delete()
            context.save()

            # Rebuild all messages from tree.
            for workflow in context.workflows.all():
                #try:
                context 
                if utils.run(context, user_args, workflow.resolver):
                    print("WORKFLOW COMPLETED")
                    context.messages.all().delete()
                    message = models.Message()
                    message.message_type = 'Notification'
                    message.response = None
                    message.content = 'Thank you for completing the workflow.'
                    message.ctx = context
                    message.save()
                #except:
                #    return Response({
                #        "status": "422",
                #        "title": "Missing Argument",
                #        "description": "<Argument: {}> is missing.".format(err.args[0].value.key)
                #    }, status=422)

        #result = getattr(operations, operation.operation)(**parameters)
        #context.values[operation.return_value.key] = result
        #context.save()

        return Response("Success")



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
            'invited_editors': [],
            'invited_reviewers': [],
            'active_editors': [],
            'active_reviewers': [],
            'finished_editors': [],
            'finished_reviewers': [],
            'review_complete': False,
            'editing_complete': False,
            'editor_count': 1,
            'reviewer_count': 1
        }
        context.save()

        for workflow in context.workflows.all():
            #try:
            utils.run(context, {}, workflow.resolver)
            #except ValueError as err:
            #    return Response({
            #        "status": "422",
            #        "title": "Missing Argument",
            #        "description": "<Argument: {}> is missing.".format(err.args[0].value.key)
            #    }, status=422)


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
