from workflow import models


def submit(**kwargs):
    def create_tokens(**kwargs):
        return None
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


def request_token(location_id=None, case=None, section="default", color={}, transition=None, **kwargs):
    def create_tokens(**kwargs):
        return None
    location = models.Location.objects.get(id=location_id)
    message = models.Message()
    message.message_type = 'Request'
    message.response = location
    message.content = location.description
    message.view = location.view
    message.section = section
    message.case = case
    message.save()
    return [{
        'name': None,
        'color': color,
        'case': case,
        'location': output,
    } for output in transition.outputs.all()]
