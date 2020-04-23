import pydnameth as pdm
from scripts.develop.routines import *


data = pdm.Data(
    path='',
    base='liver'
)

annotations = pdm.Annotations(
    name='annotations',
    type='450k',
    exclude='bad_cpgs',
    select_dict={
        'CHR': ['-X', '-Y']
    }
)

cells = pdm.Cells(
    name='cells_horvath_calculator',
    types='any'
)

observables = pdm.Observables(
    name='observables',
    types={}
)

attributes = pdm.Attributes(
    target='',
    observables=observables,
    cells=cells
)

target_list = ['gender', 'age']

data_params_list = []

data_params = get_data_params(data.base)
if data.base == 'liver':
    data_params['observables'] = ['age']
else:
    data_params['cells'] = ['Bcell', 'CD4T', 'CD8T', 'Gran', 'NK']
    data_params['observables'] = ['age']
data_params_list.append(data_params)

data_params = get_data_params(data.base)
if data.base == 'liver':
    data_params['observables'] = ['gender']
else:
    data_params['cells'] = ['Bcell', 'CD4T', 'CD8T', 'Gran', 'NK']
    data_params['observables'] = ['gender']
data_params_list.append(data_params)

pdm.residuals_table_approach_3(
    data,
    annotations,
    attributes,
    target_list,
    data_params_list,
)
