
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def api_root(request, format=None):

    return Response({
        'workflows': reverse('workflow-list', request=request, format=format),
        'operations': reverse('operation-list', request=request, format=format),
        'value': reverse('value-list', request=request, format=format),
        'contexts': reverse('context-list', request=request, format=format),
        'messages': reverse('message-list', request=request, format=format),
        'services': reverse('service-list', request=request, format=format),
        'resources': reverse('resource-list', request=request, format=format),
        'roles': reverse('role-list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
        'groups': reverse('group-list', request=request, format=format),
    })

