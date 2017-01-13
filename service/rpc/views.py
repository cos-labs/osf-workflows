from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from jsonrpcserver import methods
from api import models

@methods.add
def sendEmail():
    #models.Assignments.objects.find(
    return 'Success'


@csrf_exempt
def jsonrpc(request):
    #authorize
    #lookup assignment
    #check preconditions
    response = methods.dispatch(request.body.decode())
    return JsonResponse(response, status=response.http_status)
