import pydnameth as pdm
from scripts.develop.routines import *

data = pdm.Data(
    path='',
    base='unn_epic'
)

annotations = pdm.Annotations(
    name='annotations',
    type='850k',
    exclude='none',
    select_dict={
        'CHR': ['-X', '-Y']
    }
)

cells = pdm.Cells(
    name='',
    types='any'
)

observables = pdm.Observables(
    name='observables',
    types={}
)

attributes = pdm.Attributes(
    target='Age',
    observables=observables,
    cells=cells
)

observables_list = get_observables_list(data.base)
# observables_list = [
#     {'Sample_Group': 'C'},
#     {'Sample_Group': 'T'}
# ]
data_params = get_data_params(data.base)

pdm.observables_plot_histogram(
    data=data,
    annotations=annotations,
    attributes=attributes,
    observables_list=observables_list,
    method_params={
        'bin_size': 1.0,
        'opacity': 0.80,
        'barmode': 'overlay',
        'x_range': 'auto',
        'legend_size': 2
    }
)