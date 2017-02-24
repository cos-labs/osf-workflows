
from django.contrib.auth.models import User

from workflow import models

import logging
logger = logging.getLogger('project.interesting.stuff')



def init():
    return 'Success'


def echo(string=''):
    logger.log(10, '\necho\n====')
    return string


def accept_editor_invite(rsvp, operation=None, context=None):
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


def associate_resource(resource_identifier, operation=None, context=None):
    if resource_identifier is None:
        message = models.Message()
        message.message_type = 'Request'
        message.response = operation
        message.content = operation.description
        message.ctx = context
        message.save()
        return None
    return True


def invite_user(permit, users_to_invite, invited, role, assignments_finished, operation=None, context=None):
    if not permit:
        return invited
    if assignments_finished:
        return []
    message = models.Message()
    message.message_type = 'Request'
    message.response = operation
    message.content = operation.description
    message.ctx = context
    message.save()
    if not role:
        return invited
    if not users_to_invite:
        return invited

    for user in users_to_invite:
        if User.objects.filter(username=user.get("username", None)).exists():
            if user['username'] in invited:
                continue # The user has already been invited.
            invited.append(user["username"])
        else:
            #Handle what happens if user does not exist
            continue

    return invited


def accept_invitation(invited, invitee, rsvp, active_assignees, assignments_finished, operation=None, context=None):
    if assignments_finished:
        return []
    if invitee in invited and invitee not in active_assignees:
        active_assignees.append(invitee)
    for invite in invited:
        if invite in active_assignees:
            continue
        message = models.Message()
        message.message_type = 'Request'
        message.response = operation
        message.content = 'Hi, {}. {}'.format(invite, operation.description)
        message.ctx = context
        message.save()

    return active_assignees


def finish_assignment(active_assignees, finished_assignee, finished_assignees, assignments_finished, operation=None, context=None):
    if assignments_finished:
        return finished_assignees
    if finished_assignee in active_assignees and finished_assignee not in finished_assignees:
        finished_assignees.append(finished_assignee)
    for assignee in active_assignees:
        if assignee in finished_assignees:
            continue
        message = models.Message()
        message.message_type = 'Request'
        message.response = operation
        message.content = operation.description
        message.ctx = context
        message.save()
    return finished_assignees


def assignments_finished(finished_assignees, required_finished_assignees, operation=None, context=None):
    if len(finished_assignees) == required_finished_assignees:
        return True
    return False


def make_decision(ready_for_decision, decision, operation=None, context=None):
    if not ready_for_decision:
        return None
    message = models.Message()
    message.message_type = 'Request'
    message.response = operation
    message.content = operation.description
    message.ctx = context
    message.save()
    return True

def return_true(operation=None, context=None):
    return True


