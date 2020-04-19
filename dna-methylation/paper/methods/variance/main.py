import itertools
import numpy as np
import copy
from tqdm import tqdm
import os
from paper.infrastructure.path import get_data_path
from paper.infrastructure.load.table import load_table_dict_xlsx
from paper.infrastructure.load.annotations import load_annotations_dict
from paper.infrastructure.load.papers import load_papers_dict
from paper.infrastructure.save.table import save_table_dict_xlsx
from paper.methods.variance import get_R2s_figure
from paper.routines.infrastructure.save.figure import save_figure
import collections

R2_percentile_value = 75

data_type = 'betas'
version = 'v8'
datasets = ['GSE40279', 'GSE87571', 'EPIC', 'GSE55763']
cpg_key = 'item'

target_keys = ['increasing_fit', 'increasing_fit_id']

annotations_keys = ['CHR', 'MAPINFO', 'UCSC_REFGENE_NAME', 'UCSC_REFGENE_GROUP', 'RELATION_TO_UCSC_CPG_ISLAND']
papers_keys = ['inoshita', 'singmann', 'yousefi']

path = get_data_path() + '/draft/tables/variance/' + data_type + '/' + version

data_dicts_passed = {}
cpgs_dicts_passed = {}
R2s = {}
R2_percentiles = {}

for dataset in datasets:

    if os.path.isfile(f'{path}/{dataset}_passed.xlsx'):
        data_dict_passed = load_table_dict_xlsx(f'{path}/{dataset}_passed.xlsx')
    else:
        data_dict = load_table_dict_xlsx(f'{path}/{dataset}.xlsx')

        num_cpgs = len(data_dict[cpg_key])

        min_R2 = list(np.minimum(data_dict['best_R2_gender(F)'], data_dict['best_R2_gender(M)']))
        data_dict['min_R2'] = min_R2
        R2s[dataset] = min_R2

        R2_percentile = np.percentile(min_R2, R2_percentile_value)
        print(f'{dataset} persentile: {R2_percentile}')
        R2_percentiles[dataset] = R2_percentile

        data_dict_passed = {}
        for key in data_dict:
            data_dict_passed[key] = []

        for cpg_id in tqdm(range(0, num_cpgs), desc=f'{dataset} processing'):
            if data_dict['min_R2'][cpg_id] > R2_percentile \
                    and data_dict['number_of_clusters'][cpg_id] == 1 \
                    and data_dict['percent_of_noise_points'][cpg_id] < 1.0:

                for key in data_dict:
                    data_dict_passed[key].append(data_dict[key][cpg_id])

        save_table_dict_xlsx(f'{path}/{dataset}_passed', data_dict_passed)

    data_dicts_passed[dataset] = data_dict_passed
    cpgs_dicts_passed[dataset] = data_dict_passed[cpg_key]

if R2s:
    R2s_figure = get_R2s_figure(R2s, R2_percentiles)
    save_figure(f'{path}/R2s', R2s_figure)

cpgs_intersection = set(cpgs_dicts_passed[datasets[0]])
for dataset in datasets[1::]:
    cpgs_intersection = cpgs_intersection.intersection(cpgs_dicts_passed[dataset])

common_dict = {'i': list(cpgs_intersection)}
for key in annotations_keys:
    common_dict[key] = []
for key in target_keys:
    for dataset in data_dicts_passed:
        common_dict[f'{key}_{dataset}'] = []
common_dict['mean_I'] = []
common_dict['is_same_behaviour'] = []
for key in papers_keys:
    common_dict[key] = []

annotations_dict = load_annotations_dict()
papers_dict = load_papers_dict()

save_path = f'{path}/intersection'
if not os.path.exists(save_path):
    os.makedirs(save_path)

for cpg in tqdm(common_dict['i'], desc=f'intersection processing'):
    for key in annotations_keys:
        common_dict[key].append(annotations_dict[key][cpg])

    mean_I = 0
    is_same_behaviour = []

    for key in target_keys:
        for dataset in data_dicts_passed:
            index = data_dicts_passed[dataset][cpg_key].index(cpg)
            common_dict[f'{key}_{dataset}'].append(data_dicts_passed[dataset][key][index])
            if key == 'increasing_fit':
                mean_I += data_dicts_passed[dataset][key][index]
            elif key == 'increasing_fit_id':
                is_same_behaviour.append(data_dicts_passed[dataset][key][index])

    common_dict['mean_I'].append(mean_I / float(len(datasets)))
    counter = collections.Counter(is_same_behaviour)
    if len(counter) > 1:
        common_dict['is_same_behaviour'].append(0)
    else:
        common_dict['is_same_behaviour'].append(1)

    for paper_key in papers_keys:
        if cpg in papers_dict[paper_key]:
            common_dict[paper_key].append(1)
        else:
            common_dict[paper_key].append(0)

save_table_dict_xlsx(f'{save_path}/intersection', common_dict)
