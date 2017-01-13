# -*- coding: utf-8 -*-
"""REST API Views"""

import json

from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_json_api.views import RelationshipView
from rest_framework.exceptions import APIException

from api import models
from api import serializers

from api import task_views

@api_view(['GET'])
def api_root(request, format=None):

    return Response({
        'workflows': reverse('workflow-list', request=request, format=format),
        'tasks': reverse('task-list', request=request, format=format),
        'submissions': reverse('submission-list', request=request, format=format),
        'assignments': reverse('assignment-list', request=request, format=format),
        'roles': reverse('role-list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
    })


class Workflow(viewsets.ModelViewSet):
    queryset = models.Workflow.objects.all()
    serializer_class = serializers.Workflow


class Task(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace', 'run']
    queryset = models.Task.objects.all()
    serializer_class = serializers.Task

    def run(self, request, *args, **kwargs):
        params = json.loads(request.body)
        assignment = models.Assignment.objects.get(pk=params.pop('re_assignment', None))
        if assignment.completed:
            raise PermissionDenied()
        # TODO verify assignment is for user
        # TODO verify task is on assignment
        task = models.Task.objects.get(pk=kwargs['pk'])
        result = getattr(task_views, 'echo')(**params) 
        assignment.completed = True
        assignment.save()
        return Response(result)

    def get_queryset(self):
        queryset=self.queryset
        if 'task_pk' in self.kwargs:
            return queryset.filter(prerequisites__pk=self.kwargs['task_pk'])
        return queryset


class TaskRelationship(RelationshipView):
    queryset = models.Task.objects.all()
    serializer_class = serializers.Task


class Submission(viewsets.ModelViewSet):
    queryset = models.Submission.objects.all()
    serializer_class = serializers.Submission


class Assignment(viewsets.ModelViewSet):
    queryset = models.Assignment.objects.filter(completed=False)
    serializer_class = serializers.Assignment


class AssignmentRelationship(RelationshipView):
    queryset = models.Assignment.objects.all()


class Role(viewsets.ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = serializers.Role

class User(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.User

