# -*- coding: utf-8 -*-
'''Workflow Models'''


from itertools import chain

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User, Group
from django.db import transaction
import uuid

from workflow.utils import camelCase
#from workflow import managers
from workflow import transitions

import ipdb;

#ipdb.set_trace()

class Net(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    description = models.TextField()
    group = models.ForeignKey('auth.Group', default=1)

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
        print("Validating Net...")
        for transition in self.transitions.all():
            if not transition.inputs.exists():
                import ipdb; ipdb.set_trace()
                raise Exception

    def wake(self):

        print('\n###########################################################################')
        print('############################## WAKING NET #################################')
        print('###########################################################################\n')
        self.validate_net()

        while True:

            fireable_transitions = self.get_fireable_transitions()
            if not fireable_transitions:
                print('\n###########################################################################')
                print('############################## FIRING STALLED #############################')
                print('###########################################################################\n')
                break

            # All enabled transitions must fire during each
            # round to prevent corruption of net state.
            with transaction.atomic():

                sinks = []
                stale_tokens = []

                # Fire the transitions
                for transition in fireable_transitions:
                    print(f'\n****************************************************************')
                    print(f'Evaluating at transition {transition}...')
                    print(f'################################################################\n')
                    for case in transition.fireable_cases():
                        print(f'Evaluating case {case}')
                        tokens = []
                        for token in transition.all_tokens():
                            if token.case is not None:
                                if token.case.id == case.id:
                                    print(token)
                                    print(token.__dict__)
                                    tokens.append(token)
                        print(tokens)

                        try:
                            sink = transition.fire([token.__dict__ for token in tokens], case)
                        except Exception as e:
                            print("transition did not fire")
                            raise e

                        print(f'\nNew Tokens: {sink}')
                        # Mark tokens as stale as transitions that depend on them fire.
                        # Defer deletion until after this round of transitions have fired.
                        stale_tokens = list(chain(stale_tokens, tokens))
                        # Defer creation until after this round of transitions have fired.
                        #import ipdb; ipdb.set_trace()
                        sinks = list(chain(sinks, sink))

                # All transitions have fired, delete stale tokens
                print(f'\nDeleting stale tokens')
                for token in stale_tokens:
                    print(f'Token {token}')
                    token.delete()

                # All transitions have fired, now create tokens
                print('\nSaving newly created tokens...')
                for sink in sinks:
                    print(f'Token {sink}')
                    Token(**sink).save()

                print('')

    def __str__(self):
        return self.name



class Transition(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    description = models.TextField()
    group = models.ForeignKey('auth.Group', default=1)
    transition_class = models.CharField(max_length=128)
    inputs = models.ManyToManyField('Location', related_name='targets', through='Arc', blank=True)
    outputs = models.ManyToManyField('Location', related_name='sources', blank=True)
    net = models.ForeignKey('Net', null=True, blank=True, related_name='transitions')
    permanent_tokens = JSONField(null=True, blank=True, default=[])

    def fire(self, tokens, case):
        print(self.name)
        print(self.description)
        print(f'\nInputs:')
        for input in self.inputs.all():
            print(input)
        print('\nOutputs')
        for output in self.outputs.all():
            print(output)
        tokens.extend(self.permanent_tokens)
        print('\nTokens')
        for token in tokens:
            print(token)
        transition_fn = getattr(transitions, self.transition_class)
        print(f'\nTransition: {self.transition_class}')
        print("\n* ___ FIRING ___ *\n")
        sink = transition_fn(**{
            "tokens": tokens,
            "case": case,
            "transition": self,
        })
        return sink

    def all_tokens(self):
        tokens = []
        for arc in self.arcs.all():
            tokens = list(chain(tokens, arc.location.tokens.all()))
        print(tokens)
        return tokens

    def fireable_cases(self):
        cases = []
        print('finding fireable cases')
        for case in self.net.cases.all():
            print(f'Checking case: {case}')
            fires = True
            for arc in self.arcs.all():
                print(f"checking arc: {arc}")
                print(arc.type)
                print(arc.threshold)
                tokens = arc.location.tokens.filter(case__id=case.id)
                print(tokens)
                print(tokens.count())
                if arc.type == 'IN':
                    if tokens.count() < arc.threshold:
                        print(f'{case} is fireable')
                        continue
                if arc.type == 'EX':
                    if tokens.count() >= arc.threshold:
                        print(f'{case} is fireable')
                        continue
                fires = False
                break
            if fires:
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


class Token(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    color = JSONField(null=True, blank=True)
    case = models.ForeignKey('Case', related_name='tokens', null=True, blank=True)
    location = models.ForeignKey('Location', related_name='tokens')
    name = models.CharField(max_length=32, null=True, blank=True)
    request_messages = models.ManyToManyField('Message', null=True, blank=True, related_name='response_tokens')
    starts = models.ForeignKey('Net', related_name='starting_tokens', null=True, blank=True)
    net = models.ForeignKey('Net', related_name='tokens', null=True, blank=True)
    unique_at_location = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        for token in Token.objects.filter(location=self.location).filter(name=self.name).filter(case=self.case):
            print(f'Checking Token: {token}')
            if token.unique_at_location == True:
                print(f'Deleting Token: {token}')
                token.delete()
        super().save(*args, **kwargs)

    def __str__(self):
        return '{} @ {}'.format(self.name, self.location.name)


class Location(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    description = models.TextField()
    type = models.TextField(default='Any')
    view = models.TextField(null=True, blank=True)
    net = models.ForeignKey('Net', null=True, blank=True, related_name='locations')

    def __str__(self):
        return self.name


class Arc(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.ForeignKey('Location', related_name='arcs')
    transition = models.ForeignKey('Transition', related_name='arcs')
    net = models.ForeignKey('Net', related_name='arcs', null=True, blank=True)
    type = models.CharField(max_length=2, choices=(('IN', 'Inhibitory'), ('EX', 'Excitory')), default='EX')
    threshold = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.location.name} => {self.transition.name}'


class Case(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    net = models.ForeignKey('Net', related_name='cases', blank=True, null=True)

    def __str__(self):
        return str(self.id.urn)


class Message(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    message_type = models.CharField(max_length=24)
    timestamp = models.DateTimeField(auto_now_add=True)
    view = models.TextField(null=True, blank=True)
    case = models.ForeignKey('Case', related_name='messages')
    origin = models.ManyToManyField('Transition', related_name='messages', default=None)
    response = models.ForeignKey('Location', related_name='caller', default=None, null=True)
    response_token_name = models.CharField(max_length=128, default=None, blank=True, null=True)
    content = models.TextField()
    section = models.CharField(max_length=128, default='default')

    def __str__(self):
        return 'Message: {}'.format(self.id.urn)
