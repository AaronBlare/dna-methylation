import os
from paper.routines.infrastructure.save.table import save_table_dict_xlsx
from paper.routines.plot.venn import get_layout_3, get_layout_4, get_trace_3, get_trace_4
from paper.routines.infrastructure.save.figure import save_figure
from paper.routines.data.approaches import *
from paper.routines.data.data_dicts import *

def check_condition(data_dict):
    if data_dict['area_intersection'] < 0.5 and (abs(data_dict['slope_f']) < 0.0001 or abs(data_dict['slope_m']) < 0.0001):
        return True
    else:
        return False

type = 'betas'
names = ['GSE40279', 'GSE87571', 'EPIC', 'GSE55763']
datasets = [Dataset(type, name) for name in names]

keys_save = [
    'item',
    'aux',
    'area_intersection',
    'max_abs_slope',
    'slope_f',
    'slope_m'
]

keys_load = {}
for dataset in datasets:
    keys_load[dataset.name] = [
        'item',
        'aux',
        f'area_intersection_{get_polygon_hash(dataset)}',
        f'max_abs_slope_{get_polygon_hash(dataset)}',
        f'slope_{get_linreg_female_hash(dataset)}',
        f'slope_{get_linreg_male_hash(dataset)}'
    ]

save_path = f'{get_data_path()}/approaches/sex_specific_not_age_related/{type}'
if not os.path.exists(save_path):
    os.makedirs(save_path)

data_dicts = get_data_dicts(datasets, 'aggregator', keys_load, keys_save, get_approach_1_hash, check_condition)

cpg_dicts = get_cpg_dicts(data_dicts)

for dataset, data_dict in data_dicts.items():
    save_table_dict_xlsx(f'{save_path}/{dataset}', data_dict)

sets, sets_with_difference = get_sets(datasets, data_dicts)

save_dicts = get_cpg_dataset_save_dicts(sets, data_dicts, cpg_dicts)
curr_save_path = f'{save_path}/intersection'
if not os.path.exists(curr_save_path):
    os.makedirs(curr_save_path)
for key, save_dict in save_dicts.items():
    save_table_dict_xlsx(f'{curr_save_path}/{key}', save_dict)

save_dicts = get_cpg_dataset_save_dicts(sets_with_difference, data_dicts, cpg_dicts)
curr_save_path = f'{save_path}/intersection_with_difference'
if not os.path.exists(curr_save_path):
    os.makedirs(curr_save_path)
venn_labels = []
for key, save_dict in save_dicts.items():
    save_table_dict_xlsx(f'{curr_save_path}/{key}', save_dict)
    curr_labels = key.split('_') + [str(len(sets_with_difference[key]))]
    venn_labels.append('<br>'.join(curr_labels))

if len(datasets) == 4:
    layout = get_layout_4()
    trace = get_trace_4(venn_labels)
elif len(datasets) == 3:
    layout = get_layout_3()
    trace = get_trace_3(venn_labels)
else:
    raise ValueError(f'Venn diagram is not supported')

fig = {
    'data': [trace],
    'layout': layout,
}

save_figure(f'{save_path}/venn', fig)
