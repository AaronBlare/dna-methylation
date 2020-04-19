import numpy as np
from tqdm import tqdm
import os
from paper.infrastructure.path import get_data_path
from paper.infrastructure.load.table import load_table_dict_xlsx
from paper.infrastructure.load.annotations import load_annotations_dict
from paper.infrastructure.load.papers import load_papers_dict
from paper.infrastructure.save.table import save_table_dict_xlsx

R2_percentile_value = 90
increasing_lim = 2.0

data_type = 'residuals'
version = 'v8'
dataset = 'GSE87571'
cpg_key = 'item'

target_keys = ['increasing_fit', 'increasing_fit_id', 'min_R2']

annotations_keys = ['CHR', 'MAPINFO', 'UCSC_REFGENE_NAME', 'UCSC_REFGENE_GROUP', 'RELATION_TO_UCSC_CPG_ISLAND']
papers_keys = ['inoshita', 'singmann', 'yousefi']

path = get_data_path() + '/draft/tables/variance/' + data_type + '/' + version

if os.path.isfile(f'{path}/{dataset}_single.xlsx'):
    data_dict_passed = load_table_dict_xlsx(f'{path}/{dataset}_single.xlsx')
else:
    data_dict = load_table_dict_xlsx(f'{path}/{dataset}.xlsx')

    num_cpgs = len(data_dict[cpg_key])

    min_R2 = list(np.minimum(data_dict['best_R2_gender(F)'], data_dict['best_R2_gender(M)']))
    data_dict['min_R2'] = min_R2

    R2_percentile = np.percentile(min_R2, R2_percentile_value)
    print(f'{dataset} persentile: {R2_percentile}')

    data_dict_passed = {}
    for key in data_dict:
        data_dict_passed[key] = []

    for cpg_id in tqdm(range(0, num_cpgs), desc=f'{dataset} processing'):
        if data_dict['min_R2'][cpg_id] > R2_percentile \
                and data_dict['number_of_clusters'][cpg_id] == 1 \
                and data_dict['percent_of_noise_points'][cpg_id] < 1.0 \
                and data_dict['increasing_fit'][cpg_id] > increasing_lim:

            for key in data_dict:
                data_dict_passed[key].append(data_dict[key][cpg_id])

    save_table_dict_xlsx(f'{path}/{dataset}_single', data_dict_passed)

annotations_dict = load_annotations_dict()
papers_dict = load_papers_dict()

common_dict = {'i': list(data_dict_passed[cpg_key])}
for key in annotations_keys:
    common_dict[key] = []
for key in target_keys:
    common_dict[key] = []
for key in papers_keys:
    common_dict[key] = []


for cpg in tqdm(common_dict['i'], desc=f'intersection processing'):
    for key in annotations_keys:
        common_dict[key].append(annotations_dict[key][cpg])

    mean_I = 0
    is_same_behaviour = []

    for key in target_keys:
            index = data_dict_passed[cpg_key].index(cpg)
            common_dict[key].append(data_dict_passed[key][index])

    for paper_key in papers_keys:
        if cpg in papers_dict[paper_key]:
            common_dict[paper_key].append(1)
        else:
            common_dict[paper_key].append(0)

save_table_dict_xlsx(f'{path}/{dataset}_single_final', common_dict)
