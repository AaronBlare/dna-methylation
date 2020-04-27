import os
import pydnameth as pdm
from tqdm import tqdm
from data.infrastructure.path import get_data_path

path = f'{get_data_path()}/GPL13534/filtered'

ds_filter = {}
ds_target = {}
ds_observables = {}

fn = f'{path}/subjects.txt'
f = open(fn)
lines = f.read().splitlines()
for line in tqdm(lines, desc='datasets parsing'):
    elems = line.split('| ')
    ds = elems[0]

    if ds in ds_filter:
        ds_filter[ds].append({})
    else:
        ds_filter[ds] = [{}]
    curr_index = len(ds_filter[ds]) - 1
    if elems[1] != 'all':
        filters = elems[1].split('+ ')
        for filter in filters:
            filter_list = filter.split(': ')
            filter_key = filter_list[0]
            if filter_list[1][0] == '(' and filter_list[1][-1] == ')':
                filter_values_str = filter_list[1][1:-1]
                filter_value = filter_values_str.split(',')
            else:
                filter_value = filter_list[1]
            ds_filter[ds][curr_index][filter_key] = filter_value

    ds_target[ds] = elems[2]

    if ds in ds_observables:
        ds_observables[ds].append([])
    else:
        ds_observables[ds] = [[]]

    observables_list = elems[3].split(': ')
    observables_key = observables_list[0]
    if observables_list[1][0] == '(' and observables_list[1][-1] == ')':
        observables_values_str = observables_list[1][1:-1]
        observables_value = observables_values_str.split(',')
    else:
        print(f'Dataset {ds} observables format mismatch')
    for item in observables_value:
        curr_dict = {observables_key: item}
        curr_dict.update(ds_filter[ds][curr_index])
        ds_observables[ds][curr_index].append(curr_dict)

f.close()

tissues_folders = os.listdir(path)
ds_tissues = {}
for folder in tissues_folders:
    if os.path.isdir(f'{path}/{folder}'):
        curr_ds_list = os.listdir(f'{path}/{folder}')
        for ds in curr_ds_list:
            ds_tissues[ds] = folder

for ds in ds_tissues:
    print(ds)
    data = pdm.Data(
        path=f'{path}/{ds_tissues[ds]}',
        base=ds
    )

    for i in range(0, len(ds_observables[ds])):
        annotations = None

        cells = None

        observables = pdm.Observables(
            name='observables',
            types={}
        )

        attributes = pdm.Attributes(
            target=ds_target[data.base],
            observables=observables,
            cells=cells
        )

        observables_list = ds_observables[data.base][i]

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
