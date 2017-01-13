from jsonrpc import jsonrpc_method


jsonrpc_method('app.register')
def echo(request, param):
    return param
