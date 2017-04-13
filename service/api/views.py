
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def api_root(request, format=None):

    return Response({
        'workflows': reverse('net-list', request=request, format=format),
        'transitions': reverse('transition-list', request=request, format=format),
        'locations': reverse('location-list', request=request, format=format),
        'arcs': reverse('arc-list', request=request, format=format),
        'messages': reverse('message-list', request=request, format=format),
        'cases': reverse('case-list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
        'tokens': reverse('token-list', request=request, format=format),
        'groups': reverse('group-list', request=request, format=format),
    })

