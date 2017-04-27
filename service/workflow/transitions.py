from itertools import chain
from workflow import models


def submit(**kwargs):

    def create_tokens(**kwargs):
        return None
    return []
    #{
    #    'name': 'Author',
    #    'color': 'John Doe'
    #}


def flatten_tokens(tokens=[], case=None, transition=None, *args, **kwargs):
    ''' location = models.Location.objects.get(id=token['color']['location'])
    message = models.Message()
    message.message_type = 'Request'
    message.response = location
    message.content = location.description
    message.view = location.view
    message.section = token['color']['section']
    try:
        message.response_token_name = token['color']['token_name']
    except error as e:
        print(f'{transition} caused error {e}; no token name')
        raise
    message.case = case
    message.save()
    '''
    return []


def add_item_to_collection(**kwargs):

    def create_tokens(**kwargs):
        return None
    return []


def passthru(tokens=[], case=None, transition=None, **kwargs):

    sinks = []
    for token in tokens:
        sinks.extend([{
            'name': token['name'],
            'color': token['color'],
            'case': case,
            'location': output,
        } for output in transition.outputs.all()])
    return sinks


def trigger(tokens=[], case=None, transition=None, **kwargs):
    sinks = []
    for token in tokens:
        if token['name'] == 'destroy_token_request':
            location = models.Location.objects.get(id=token['color']['location'])
            for token_request in location.tokens.filter(case=case).filter(name=token['color']['token_name']):
                try:
                    models.Message.objects.get(id=token_request.color).delete()
                    token_request.delete()
                except Exception as e:
                    print(e)
                    print(token_request)
                    print(token_request.color)
                    import ipdb; ipdb.set_trace()
        if token.get('name') == 'token_request_location':
            location = models.Location.objects.get(id=token['color']['location'])
            message = models.Message()
            message.message_type = 'Request'
            message.response = location
            message.content = location.description
            message.view = location.view
            message.section = token['color']['section']
            try:
                message.response_token_name = token['color']['token_name']
            except Exception as e:
                print(f'{transition} caused error {e}; no token name')
                raise
            message.case = case
            message.save()
            sinks.extend([{
                'name': 'request_pointer',
                'color': str(message.id),
                'case': case,
                'location': output,
                'unique_at_location': token['color']['unique']
            } for output in transition.outputs.all()])
        token_location_id = token.get('location_id')
        if token_location_id is None:
            continue
        token_location = models.Location.objects.get(id=token['location_id'])
        sinks.extend([{
            'name': token['name'],
            'color': token['color'],
            'case': case,
            'location': token_location,
            'unique_at_location': token['unique_at_location']
        }])
    #sinks.extend([{
    #    'name': 'Triggered',
    #    'color': None,
    #    'case': case,
    #    'location': output,
    #    'unique_at_location': True
    #} for output in transition.outputs.all()])
    return sinks


def request_tokens(tokens=[], case=None, transition=None, **kwargs):

    sinks = []
    for token in tokens:
        #import ipdb; ipdb.set_trace()
        if token['name'] == 'token_request_location':
            location = models.Location.objects.get(id=token['color']['location'])
            message = models.Message()
            message.message_type = 'Request'
            message.response = location
            message.content = location.description
            message.view = location.view
            message.section = token['color']['section']
            try:
                message.response_token_name = token['color']['token_name']
            except error as e:
                print(f'{transition} caused error {e}; no token name')
                raise
            message.case = case
            message.save()
            sinks.extend([{
                'name': 'request_pointer',
                'color': str(message.id),
                'case': case,
                'location': output,
                'unique_at_location': token['color']['unique']
            } for output in transition.outputs.all()])
        if token['name'] == 'destroy_token_request':
            location = models.Location.objects.get(id=token['color']['location'])
            for token_request in location.tokens.filter(case=case).filter(name=token['color']['token_name']):
                models.Message.objects.get(id=token_request.color).delete()
                token_request.delete()

    return sinks


def delete_token_request(tokens=[], case=None, transition=None, **kwargs):

    sinks = []
    for token in tokens:
        if token['name'] == "request_pointer":
            models.Message.objects.delete(id=token['color'])
            sinks.extend([{
                'name': None,
                'color': None,
                'case': case,
                'location': output,
            } for output in transition.outputs.all()])
    return sinks
