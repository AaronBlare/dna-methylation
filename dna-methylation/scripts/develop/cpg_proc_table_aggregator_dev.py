import pydnameth as pdm

data = pdm.Data(
    name='cpg_beta',
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

observables_list = [
    {'gender': 'F'},
    {'gender': 'M'}
]

pdm.cpg_proc_table_aggregator_dev(
    data=data,
    annotations=annotations,
    attributes=attributes,
    observables_list=observables_list,
    params=None
)