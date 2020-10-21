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
    name='cell_counts',
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

target_ss = 'Sex'
target_ar = 'Age'

data_params_ss = get_data_params(data.base)
data_params_ss['cells'] = ['Bcell', 'CD4T', 'CD8T', 'Mono', 'Neu', 'NK']
data_params_ss['observables'] = ['Age']

data_params_ar = get_data_params(data.base)
data_params_ar['cells'] = ['Bcell', 'CD4T', 'CD8T', 'Mono', 'Neu', 'NK']
data_params_ar['observables'] = ['Sex']

pdm.residuals_table_approach_3(
    data,
    annotations,
    attributes,
    target_ss,
    target_ar,
    data_params_ss,
    data_params_ar
)
