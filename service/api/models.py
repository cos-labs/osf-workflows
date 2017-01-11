# -*- coding: utf-8 -*-
"""REST API Models"""


from django.db import models


class Workflow(models.Model):

    name = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name



class Task(models.Model):

    name = models.TextField()
    description = models.TextField()
    workflow = models.ManyToManyField(
        'Workflow',
        related_name='tasks',
        blank=True
    )
    subtasks = models.ManyToManyField(
        'Task',
        related_name='parent_task',

        blank=True
    )
    prerequisites = models.ManyToManyField(
        'Task',
        related_name='prerequisite_for',
        blank=True
    )
    #actions = models.ManyToManyField(
    #    'Action',
    #    related_name='tasks',
    #    blank=True
    #)
    view = models.TextField()
    splay = models.IntegerField(default=1)
    cycle = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        #if self.prerequisites:
        super(Task, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Submission(models.Model):

    identifier = models.TextField()
    uploader = models.ForeignKey(
        'auth.User',
        related_name='submissions',
        default=None,
        null=True,
        blank=True
    )
    workflow = models.ForeignKey(
        'Workflow',
        related_name='submissions',
        default=None
    )
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.identifier


class Assignment(models.Model):

    submission = models.ForeignKey(
        'Submission',
        related_name='assignments',
        default=None
    )
    task = models.ForeignKey(
        'Task',
        related_name='assignments'
    )
    assignee = models.ForeignKey(
        'auth.User',
        related_name='assignments',
        default=None
    )
    role = models.ForeignKey(
        'Role',
        related_name='assignments',
        default=None
    )
    completed = models.BooleanField(default=False)

    unique_together = (
        'submission',
        'task',
        'assignee',
        'role'
    )

    def __str__(self):
        return '{} assigned to {} as {} on {}.'.format(
            self.assignee.username,
            self.task.name,
            self.role.name,
            self.submission.identifier
        )


class Role(models.Model):

    name = models.TextField()
    responsibilities = models.TextField()

    def __str__(self):
        return self.name
