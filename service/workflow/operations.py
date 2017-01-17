
from django.contrib.auth.models import User

from workflow import models

import logging
logger = logging.getLogger('project.interesting.stuff')



def init():
    return 'Success'


def echo(string=''):
    logger.log(10, '\necho\n====')
    return string


def accept_editor_invite(rsvp):
    next_assignment = models.Assignment()
    if rsvp == 'Accept':
        next_assignment.task = models.Task.objects.get(pk=7)
    if rsvp == 'Decline':
        next_assignment.task = models.Task.objects.get(pk=5)
    next_assignment.assignee = User.objects.get(pk=1)
    next_assignment.submission = models.Submission.objects.get(pk=1)
    next_assignment.role = models.Role.objects.get(pk=1)
    next_assignment.save()
    return 'Success'


def editor_invite():
    return True


def link_resource():
    return 'Resource Linked'

def IO():
    return
#

