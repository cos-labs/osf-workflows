# -*- coding: utf-8 -*-
"""REST API Serializers"""


from rest_framework_json_api import serializers, relations
from django.contrib.auth.models import User

from api import models


class Workflow(serializers.ModelSerializer):

    tasks = relations.ResourceRelatedField(
        many=True,
        queryset=models.Task.objects.all(),
    )

    class Meta:
        model = models.Workflow
        fields = (
            'name',
            'description',
            'tasks'
        )

    class JSONAPIMeta:
        resource_name = "workflows"


class Task(serializers.ModelSerializer):

    prerequisites = relations.ResourceRelatedField(
        many=True,
        queryset=models.Task.objects.all(),
    )

    class Meta:
        model = models.Task
        fields = (
            'name',
            'description',
            'workflow',
            'subtasks',
            'parent_task',
            'prerequisites',
            'prerequisite_for',
            'view'
        )

    class JSONAPIMeta:
        resource_name = 'tasks'


class Submission(serializers.ModelSerializer):

    class Meta:
        model = models.Submission
        fields = (
            'identifier',
            'uploader',
            'workflow',
            'upload_date'
        )

    class JSONAPIMeta:
        resource_name = 'submissions'


class Assignment(serializers.ModelSerializer):

    submission = relations.ResourceRelatedField(
        many=False,
        queryset=models.Submission.objects,
    )

    class Meta:
        model = models.Assignment
        fields = (
            'submission',
            'task',
            'assignee',
            'role',
            'completed'
        )

    class JSONAPIMeta:
        resource_name = 'assignments'


class Role(serializers.ModelSerializer):

    class Meta:
        model = models.Role
        fields = (
            'name',
            'responsibilities'
        )

    class JSONAPIMeta:
        resource_name = 'roles'


class User(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
        )

    class JSONAPIMeta:
        resource_name = 'users'
