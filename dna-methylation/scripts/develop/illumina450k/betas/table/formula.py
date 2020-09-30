import pydnameth as pdm
from scripts.develop.routines import *


data = pdm.Data(
    path='',
    #path='E:/YandexDisk/Work/pydnameth/tissues/brain(DLPFC)',
    #base='GSE87571'
    base='liver'
    #base='GSE74193'
)

annotations = pdm.Annotations(
    name='annotations',
    type='450k',
    exclude='bad_cpgs',
    select_dict={
        'CHR': ['-X', '-Y']
    }
)

observables = pdm.Observables(
    name='observables',
    #name='observables_part(control)',
    types={}
    #types={'group': 'Control'}
)

cells = pdm.Cells(
    #name='cells_horvath_calculator',
    name='',
    types='any'
)

target = get_target(data.base)
attributes = pdm.Attributes(
    target=target,
    observables=observables,
    cells=cells
)

method_params = {
    'observables': ['age', 'gender'],
    #'observables': ['age', 'sex'],
    #'cells': ['Bcell', 'CD4T', 'CD8T', 'Gran', 'NK']
    #'cells': ['propNeuron']
}

data_params = get_data_params(data.base)

pdm.betas_table_formula(
    data=data,
    annotations=annotations,
    attributes=attributes,
    data_params=data_params,
    method_params=method_params,
)