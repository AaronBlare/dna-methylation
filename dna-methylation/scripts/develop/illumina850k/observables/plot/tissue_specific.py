import pydnameth as pdm
from tqdm import tqdm

path = 'E:/YandexDisk/Work/pydnameth/script_datasets/GPL13534/filtered'

ds_filter = {}
ds_target = {}
ds_observables = {}

fn = f'{path}/subjects.txt'
f = open(fn)
lines = f.read().splitlines()
for line in tqdm(lines, desc='datasets parsing'):
    elems = line.split('| ')
    ds = elems[0]

    ds_filter[ds] = {}
    if elems[1] != 'all':
        filters = elems[1].split(', ')
        for filter in filters:
            filter_list = filter.split(': ')
            filter_key = filter_list[0]
            if '(' in filter_list[1] and ')' in filter_list[1]:
                filter_values_str = filter_list[1][1::-1]
                filter_value = filter_values_str.split(',')
            else:
                filter_value = filter_list[1]
            ds_filter[ds][filter_key] = filter_value

ololo = 1

f.close()




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