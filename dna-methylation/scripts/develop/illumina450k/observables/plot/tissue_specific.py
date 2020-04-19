import pydnameth as pdm

data = pdm.Data(
    path='E:/YandexDisk/Work/pydnameth/script_datasets/GPL13534/filtered/airway_epithelial_cells',
    base='GSE85566'
)

annotations = None

cells = None

observables = pdm.Observables(
    name='observables',
    types={}
)

attributes = pdm.Attributes(
    target='age',
    observables=observables,
    cells=cells
)

observables_list = [
    {'gender': 'Female', 'disease status': 'Control'},
    {'gender': 'Male', 'disease status': 'Control'}
]

data_params = None

pdm.observables_plot_histogram(
    data=data,
    annotations=annotations,
    attributes=attributes,
    observables_list=observables_list,
    method_params={
        'bin_size': 1.0,
        'opacity': 0.80,
        'barmode': 'overlay',
        'x_range': [0, 110],
        'legend_size': 1
    }
)