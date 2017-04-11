from workflow import models


def submit(**kwargs):
    def create_tokens(**kwargs):
        return None
    import ipdb; ipdb.set_trace()
    return {
        'name': 'Author',
        'color': 'John Doe'
    }


def add_item_to_collection(**kwargs):
    def create_tokens(**kwargs):
        return None
    return create_tokens


def passthru(**kwargs):
    def create_tokens(**kwargs):
        return None
    return create_tokens


def request_token(**kwargs):
    def create_tokens(**kwargs):
        return None
    #message = models.Message()
    #message.message_type = 'Request'
    #import ipdb; ipdb.set_trace()
    #message.response = operation
    #message.content = operation.description
    #message.ctx = context
    #message.save()
    return {
        'name': None,
        'color': kwargs
    }
