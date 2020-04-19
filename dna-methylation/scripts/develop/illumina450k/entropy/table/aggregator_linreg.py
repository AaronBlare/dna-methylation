import pydnameth as pdm

data_sets = ['GSE87571_TEST']

for data_set in data_sets:

    data = pdm.Data(
        path='',
        base=data_set
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
        types={}
    )

    if data.base == 'GSE55763':
        observables_list = [
            {'gender': 'F', 'is_duplicate': '0', 'age': (35, 100)},
            {'gender': 'M', 'is_duplicate': '0', 'age': (35, 100)}
        ]
    else:
        observables_list = [
            {'gender': 'F'},
            {'gender': 'M'}
        ]

    data_params = {
        'data': 'betas_adj',
        'observables': ['age'],
        'cells': ['Bcell', 'CD4T', 'NK', 'CD8T', 'Gran']
    }

    cells = pdm.Cells(
        name='cells_horvath_calculator',
        types='any'
    )

    attributes = pdm.Attributes(
        target='age',
        observables=observables,
        cells=cells
    )

    pdm.entropy_table_aggregator_linreg(
        data=data,
        annotations=annotations,
        attributes=attributes,
        observables_list=observables_list,
        data_params=data_params
    )