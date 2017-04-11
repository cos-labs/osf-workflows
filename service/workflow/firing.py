import numpy

inputs = [[0 if value in transition.inputs else 1 for value in net.values] for transition in net.transitions]
outputs = [[0 if value in transition.outputs else 1 for value in net.values] for transition in net.transitions]

# Stored on the workflow; update on workflow modification
composite_change = numpy.matrix(outputs) - numpy.matrix(inputs)

firing_matrix = [1 if transition.fires() else 0 for transition in net.transitions]
state_matrix =  net.values

contitions
values





# -340
