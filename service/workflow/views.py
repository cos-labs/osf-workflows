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


class Net(viewsets.ModelViewSet):
    queryset = models.Net.objects.all()
    serializer_class = serializers.Net


class Transition(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace', 'run']
    queryset = models.Transition.objects.all()
    serializer_class = serializers.Transition

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
        context = models.Case.objects.get(pk=user_args.pop('ctx', None))
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

        return Response("Success")



class TransitionRelationship(RelationshipView):
    queryset = models.Transition.objects.all()
    serializer_class = models.Transition


class Location(viewsets.ModelViewSet):
    queryset = models.Location.objects.all()
    serializer_class = serializers.Location


class Arc(viewsets.ModelViewSet):
    queryset = models.Arc.objects.all()
    serializer_class = serializers.Arc


class Case(viewsets.ModelViewSet):
    queryset = models.Case.objects.all()
    serializer_class = serializers.Case

    def perform_create(self, serializer):

        case = serializer.save()

        # Set up tokens in net's default token configuration
        for token in case.net.starting_tokens.all():
            models.Token(
                color=token.color,
                case=case,
                location=token.location,
                name=token.name
            ).save()
            import ipdb; ipdb.set_trace()

        case.net.wake()

        # [{
        #    'name': 'Editor Role',
        #    'color': 'Editor',
        #}, {
        #    'name': 'Reviewer Role',
        #    'color': 'Reviewer',
        #}, {
        #    'invited_editors': [],
        #    'invited_reviewers': [],
        #    'active_editors': [],
        #    'active_reviewers': [],
        #    'finished_editors': [],
        #    'finished_reviewers': [],
        #    'review_complete': False,
        #    'editing_complete': False,
        #    'editor_count': 1,
        #    'reviewer_count': 1,
        #    'indicated_disciplines': [],
        #    'connection_methods': [
        #        'upload',
        #        'connect_existing'
        #     ],
        #    'preprint_title': False
        #}]:

    def perform_update(self, serializer):

        case = serializer.save()

        # Initialize any tokens that are IO
        for location in self.locations.all():
            if location.type == "IO":
                pass
                #Token(color=None, case=self, location=location, name='mytoken').save()

        case.net.wake()


class Message(viewsets.ModelViewSet):
    queryset = models.Message.objects.all()
    serializer_class = serializers.Message

    def get_queryset(self):
        queryset = self.queryset
        return queryset


class User(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.User


class Group(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.Group
