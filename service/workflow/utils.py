from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response

from workflow import operations


def run(context, user_args, operation, visited=None):
    if visited is None:
        visited = []
    visited.append(operation)
    print(visited)

    args = {}

    for param in operation.parameters.all():

        key = param.name
        value = param.value
        _value = context.values.get(value.key, None)

        if param.value.type.split(' ')[0] == 'IO':
            args[param.name] = user_args.get(param.name, None)
            continue

        if value.type.split(' ')[0] == 'Volatile':
            volatile_operation = getattr(value, 'source_operation', None)
            if volatile_operation and volatile_operation not in visited:
                args[key] = run(context, user_args, volatile_operation, visited)
                continue

        if _value is not None:
            if _value is not "_VISITED_":
                args[key] = _value
                continue

        source_operation = getattr(value, 'source_operation', None)
        if source_operation and source_operation not in visited:
            args[key] = run(context, user_args, source_operation, visited)
            continue

        print("args[key] is set to None here")
        args[key] = None

    permit = True
    for param in operation.parameters.all():
        key = param.name
        value = param.value
        if args.get(key, None) is None:
            if value.type.split(' ')[0] == 'IO':
                continue
            permit = False
            break

    if permit:
        print("====================================================================================================")
        print("")
        print(operation.name)
        print("{} was RUN.".format(operation.operation))
        print(args)
        print("")
        print(context.values)
        print("")
        print("")
        result = getattr(operations, operation.operation)(operation=operation, context=context, **args)
        if operation.return_value:
            context.values[operation.return_value.key] = result
            context.save()
    else:
        print("====================================================================================================")
        print("")
        print(operation.name)
        print("{} was DEFERRED.".format(operation.operation))
        print(args)
        print("")
        print(context.values)
        print("")
        print("")
        if operation.return_value:
            result = context.values.get(operation.return_value.key, None)
        else:
            result = None
            print("parameters[key] is set to None by result")

    return result


def camelCase(st):
    output = ''.join(x for x in st.title() if x.isalpha())
    return output[0].lower() + output[1:]
