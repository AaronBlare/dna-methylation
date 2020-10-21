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
    name='cells_horvath_calculator',
    types='any'
)

target = get_target(data.base)
data_params = get_data_params(data.base)

# observables_list = [
#     {'Sex': 'F'},
#     {'Sex': 'M'},
# ]

observables_list = [
    {'Sex': 'any'},
]

for obs in observables_list:

    observables = pdm.Observables(
        name='observables',
        types=obs
    )

    attributes = pdm.Attributes(
        target=target,
        observables=observables,
        cells=cells
    )

    pdm.betas_table_linreg(
        data=data,
        annotations=annotations,
        attributes=attributes,
        data_params=data_params
    )