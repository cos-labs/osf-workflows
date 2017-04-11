# -*- coding: utf-8 -*-
'''Workflow Models'''


from itertools import chain

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User, Group
from django.db import transaction
import uuid

from workflow.utils import camelCase
from workflow import managers
from workflow import transitions


class Net(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    description = models.TextField()
    group = models.ForeignKey('auth.Group', default=1)
    starting_tokens = models.ManyToManyField('Token', blank=True)

    def get_fireable_transitions(self):
        transitions = [transition for transition in self.transitions.all() if transition.is_fireable()]
        print(transitions)
        return transitions

    def get_enabled_transitions(self):
        return [transition for transition in self.transitions.all() if transition.is_enabled()]

    def fire_all(self):
        pass

    def fire(self):
        fireable_transitions = self.get_fireable_transitions()
        consumed_tokens = Token.objects.none()

    def validate_net(self):
        for transition in self.transitions.all():
            if not transition.inputs.exists():
                import ipdb; ipdb.set_trace()
                raise Exception

    def wake(self):

        self.validate_net()

        while True:

            fireable_transitions = self.get_fireable_transitions()
            if not fireable_transitions:
                break

            # All transitions must fire during each round to prevent corruption of net state.
            with transaction.atomic():

                sinks = []
                stale_tokens = []

                # Fire the transitions
                for transition in fireable_transitions:
                    print(f'{transition}')
                    for case in transition.fireable_cases():
                        tokens = []
                        for token in transition.all_tokens():
                            print(f'Got token: {token}')
                            if token.case is not None:
                                print(f'{token.case.id} {case.id}')
                                tokens.append(token)
                                if token.case.id == case.id:
                                    print(tokens)
                        sink = transition.fire(tokens)
                        # Mark tokens as stale as transitions that depend on them fire.
                        # Defer deletion until after this round of transitions have fired.
                        stale_tokens = list(chain(stale_tokens, tokens))
                        # Defer creation until after this round of transitions have fired.
                        sinks.append(sink)

                # All transitions have fired, delete stale tokens
                for token in stale_tokens:
                    token.delete()

                # All transitions have fired, now create tokens
                for sink in sinks:
                    print('--Fired--')
                    print(f'consumed_tokens: {sink}')

        # Sustained firing is done. Allow user to begin interacting with net again.
        for transition in self.get_enabled_transitions():
            for case in transition.enabled_cases():
                case.enable_transition(transition)

    def __str__(self):
        return self.name


class Transition(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    description = models.TextField()
    group = models.ForeignKey('auth.Group', default=1)
    section = models.CharField(max_length=128, default='default')
    transition_class = models.CharField(max_length=128)
    inputs = models.ManyToManyField('Location', related_name='targets', through='Arc', blank=True)
    outputs = models.ManyToManyField('Location', related_name='sources', blank=True)
    net = models.ForeignKey('Net', null=True, blank=True, related_name='transitions')
    view = models.TextField(null=True, blank=True)

    def fire(self, transition_tokens):
        return getattr(transitions, self.transition_class)(**{token.name: token.color for token in transition_tokens})

    def all_tokens(self):
        tokens = Token.objects.none()
        for arc in self.arcs.all():
            tokens = list(chain(tokens, arc.location.tokens.all()))
        print(tokens)
        return tokens

    def fireable_cases(self):
        querysets = [arc.location.tokens.all() for arc in self.arcs.all()]
        cases = []
        for case in self.net.cases.all():
            if all([queryset.filter(case__id=case.id).exists() for queryset in querysets]):
                print(case)
                cases.append(case)
        return cases

    def enabled_cases(self):
        querysets = [arc.location.tokens.all() for arc in self.arcs.all() if arc.location.type != 'IO']
        return [case for case in self.net.cases.all() if
            all([queryset.filter(case__id=case.id).exists() for queryset in querysets])]

    def is_fireable(self):
        return any(self.fireable_cases())

    def is_enabled(self):
        return any(self.enabled_cases())

    def __str__(self):
        return self.name




        '''

            for case in self.cases:
                location_tokens = arc.location.tokens.filter(case__id=case.id)
                token_count = location_tokens.count()

                print(f'{token_count} {location_tokens.all()} {arc.location.type} {arc.type} {arc.threshold}')

                if arc.type == 'IN':
                    if token_count >= arc.threshold:
                        enabled = False
                        continue

                if arc.type == 'EX':
                    if token_count < arc.threshold:
                        enabled = False
                        continue

                transition_tokens = transition_tokens.union(location_tokens)
        case_tokens = self.get_tokens.filter(case__id=case.id)
        transition_tokens = self.get_tokens()
        '''




class Token(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    color = JSONField(null=True, blank=True)
    case = models.ForeignKey('Case', related_name='tokens', null=True, blank=True)
    location = models.ForeignKey('Location', related_name='tokens')
    name = models.CharField(max_length=32, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.value.key
        super().save(*args, **kwargs)

    def __str__(self):
        return '{} @ {}'.format(self.name, self.location.name)


class Location(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    description = models.TextField()
    type = models.TextField(default='Any')
    net = models.ForeignKey('Net', null=True, blank=True, related_name='locations')

    def __str__(self):
        return self.name


class Arc(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.ForeignKey('Location', related_name='arcs')
    transition = models.ForeignKey('Transition', related_name='arcs')
    type = models.CharField(max_length=2, choices=(('IN', 'Inhibitory'), ('EX', 'Excitory')), default='EX')
    threshold = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.location.name} => {self.transition.name}'


class Case(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    net = models.ForeignKey('Net', related_name='cases', blank=True, null=True)

    def enable_transition(self, transition):
        message = Message()
        message.message_type = 'Request'
        message.response = transition
        message.content = transition.description
        message.case = self
        message.save()

    def __str__(self):
        return str(self.id.urn)


class Message(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    message_type = models.CharField(max_length=24)
    timestamp = models.DateTimeField(auto_now_add=True)
    case = models.ForeignKey('Case', related_name='messages')
    origin = models.ManyToManyField('Transition', related_name='messages', default=None)
    response = models.ForeignKey('Transition', related_name='caller', default=None, null=True)
    content = models.TextField()

    def __str__(self):
        return 'Message: {}'.format(self.id.urn)
