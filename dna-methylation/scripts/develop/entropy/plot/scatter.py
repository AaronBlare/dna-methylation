import pydnameth as pdm

data = pdm.Data(
    path='',
    base='GSE87571'
)

annotations = pdm.Annotations(
    name='annotations',
    exclude='bad_cpgs',
    cross_reactive='any',
    snp='any',
    chr='NS',
    gene_region='any',
    geo='any',
    probe_class='any'
)

observables = pdm.Observables(
    name='observables',
    types={}
)

cells = pdm.Cells(
    name='cells',
    types='any'
)

attributes = pdm.Attributes(
    target='age',
    observables=observables,
    cells=cells
)

if data.base == 'GSE55763':
    observables_list = [
        {'gender': 'F', 'is_duplicate': '0'},
        {'gender': 'M', 'is_duplicate': '0'}
    ]
else:
    observables_list = [
        {'gender': 'F'},
        {'gender': 'M'}
    ]

data_params = {
    'data': 'betas_adj',
    'observables': ['age'],
    'cells': ['B', 'CD4T', 'NK', 'CD8T', 'Gran']
}

pdm.entropy_plot_scatter(
    data=data,
    annotations=annotations,
    attributes=attributes,
    observables_list=observables_list,
    data_params=data_params,
    method_params={
        'x_range': [5, 105],
        'y_range': 'auto',
    }
)