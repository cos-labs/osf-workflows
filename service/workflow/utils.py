from django.core.exceptions import ObjectDoesNotExist


def get_allowed_operations(context, operation):

    allowed_operations = []
    parameters = operation.parameters.all()
    parameters_checklist = list(parameters) # Make a copy so we don't modify the original

    #import ipdb; ipdb.set_trace()

    for index, value in enumerate(parameters_checklist):
        parameters_checklist[index] = False
        if context.values.get(value.key, None) is not None:
            parameters_checklist[index] = True
        if value.type.split(' ')[0] == 'IO':
            parameters_checklist[index] = True
        if not hasattr(value, 'source_operation'):
            parameters_checklist[index] = True

    if all(parameter == True for parameter in parameters_checklist):
        allowed_operations.append(operation)
    else:
        for parameter in parameters:
            operation = getattr(parameter, 'source_operation', None)
            if operation:
                allowed_operations.extend(get_allowed_operations(context, operation))

    return allowed_operations


def camelCase(st):
    output = ''.join(x for x in st.title() if x.isalpha())
    return output[0].lower() + output[1:]
