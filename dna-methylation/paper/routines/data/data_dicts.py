import copy
import itertools
from paper.routines.infrastructure.save.table import save_table_dict_xlsx
from paper.routines.infrastructure.load.table import load_table_dict_pkl
from paper.routines.infrastructure.load.annotations import load_annotations_dict
from paper.routines.infrastructure.load.papers import load_papers_dict
from paper.routines.infrastructure.path import get_data_path
from paper.routines.plot.venn import get_layout_2, get_layout_3, get_layout_4, get_trace_2, get_trace_3, get_trace_4
from paper.routines.infrastructure.save.figure import save_figure
from collections import defaultdict
from tqdm import tqdm
import numpy as np
import os


class Dataset:
    def __init__(self, type, name):
        self.type = type
        self.name = name


def get_data_dicts(datasets, method, keys_load, keys_save, hash_fun):

    data_dicts = {}
    for ds_id, dataset in enumerate(datasets):

        curr_load_path = f'{get_data_path()}/{dataset.name}/{dataset.type}/table/{method}/{hash_fun(dataset)}'
        data_dict = load_table_dict_pkl(f'{curr_load_path}/default.pkl')

        data_dicts[dataset.name] = defaultdict(list)

        num_cpgs = len(data_dict[keys_load[dataset.name][0]])

        for cpg_id in tqdm(range(0, num_cpgs), desc=f'{dataset.name} processing'):
            for key_id, key in enumerate(keys_save):
                data_dicts[dataset.name][key].append(data_dict[keys_load[dataset.name][key_id]][cpg_id])

    return data_dicts


def get_sets(data_dicts, item_key='item'):

    names = [ds for ds in data_dicts]
    datasets_ids = list(range(0, len(names)))
    keys_ordered = copy.deepcopy(names)
    sets = {}
    checking = {}
    for name in names:
        sets[name] = set(data_dicts[name][item_key])
        checking[name] = 0

    for L in range(2, len(names) + 1):
        for subset in itertools.combinations(datasets_ids, L):

            curr_ids = list(subset)

            curr_key_raw = np.sort(np.array(names)[np.array(curr_ids)])
            curr_key = '_'.join(list(curr_key_raw))

            if curr_key not in sets:

                cur_intersection = set(data_dicts[names[curr_ids[0]]][item_key])
                for id in curr_ids[1::]:
                    cur_intersection = cur_intersection.intersection(set(data_dicts[names[id]][item_key]))
                sets[curr_key] = cur_intersection

                keys_ordered.append(curr_key)

    keys_ordered = keys_ordered[::-1]

    sets_with_difference = copy.deepcopy(sets)
    for key in keys_ordered:
        curr_labels = set(key.split('_'))
        for key_var in keys_ordered:
            curr_labels_var = set(key_var.split('_'))
            if key_var != key:
                if curr_labels.issubset(curr_labels_var):
                    sets_with_difference[key] -= sets_with_difference[key_var]

    for set_key in sets_with_difference:
        curr_labels = set_key.split('_')
        for label in curr_labels:
            checking[label] += len(sets_with_difference[set_key])

    for name in names:
        if checking[name] != len(set(data_dicts[name][item_key])):
            raise ValueError('Error in venn data creating')

    return sets, sets_with_difference


def get_cpg_dicts(data_dicts,  key='item'):
    cpg_dicts = {}
    for dataset in data_dicts:
        cpg_dicts[dataset] = {}
        num_items = 0
        for item in data_dicts[dataset][key]:
            cpg_dicts[dataset][item] = num_items
            num_items += 1
    return cpg_dicts


def get_cpg_save_dicts(sets, data_dicts, cpg_dicts, key='item'):

    annotations_keys = ['CHR', 'MAPINFO', 'UCSC_REFGENE_NAME', 'UCSC_REFGENE_GROUP', 'RELATION_TO_UCSC_CPG_ISLAND']
    papers_keys = ['inoshita', 'singmann', 'yousefi']
    annotations_dict = load_annotations_dict()
    papers_dict = load_papers_dict()

    save_dicts = {}

    for set_key in sets:

        save_dicts[set_key]= {}

        for metrics_key in [key] + annotations_keys + papers_keys:
            save_dicts[set_key][metrics_key] = []

        curr_datasets = set_key.split('_')
        for dataset in curr_datasets:
            for ds_key in data_dicts[dataset]:
                if ds_key not in save_dicts[set_key]:
                    save_dicts[set_key][ds_key + '_' + dataset] = []

        for cpg in sets[set_key]:
            save_dicts[set_key][key].append(cpg)
            for dataset in curr_datasets:
                for ds_key in data_dicts[dataset]:
                    if ds_key not in save_dicts[set_key]:
                        save_dicts[set_key][ds_key + '_' + dataset].append(
                            data_dicts[dataset][ds_key][cpg_dicts[dataset][cpg]])
            for ann_key in annotations_keys:
                save_dicts[set_key][ann_key].append(annotations_dict[ann_key][cpg])
            for paper_key in papers_keys:
                if cpg in papers_dict[paper_key]:
                    save_dicts[set_key][paper_key].append(1)
                else:
                    save_dicts[set_key][paper_key].append(0)

    return save_dicts


def process_intersections(data_dicts, save_path):
    cpg_dicts = get_cpg_dicts(data_dicts)

    for dataset, data_dict in data_dicts.items():
        save_table_dict_xlsx(f'{save_path}/{dataset}', data_dict)

    sets, sets_with_difference = get_sets(data_dicts)

    save_dicts = get_cpg_save_dicts(sets, data_dicts, cpg_dicts)
    curr_save_path = f'{save_path}/intersection'
    if not os.path.exists(curr_save_path):
        os.makedirs(curr_save_path)
    for key, save_dict in save_dicts.items():
        save_table_dict_xlsx(f'{curr_save_path}/{key}', save_dict)

    save_dicts = get_cpg_save_dicts(sets_with_difference, data_dicts, cpg_dicts)
    curr_save_path = f'{save_path}/intersection_with_difference'
    if not os.path.exists(curr_save_path):
        os.makedirs(curr_save_path)
    venn_labels = []
    for key, save_dict in save_dicts.items():
        save_table_dict_xlsx(f'{curr_save_path}/{key}', save_dict)
        curr_labels = key.split('_') + [str(len(sets_with_difference[key]))]
        venn_labels.append('<br>'.join(curr_labels))

    if len(data_dicts) == 4:
        layout = get_layout_4()
        trace = get_trace_4(venn_labels)
    elif len(data_dicts) == 3:
        layout = get_layout_3()
        trace = get_trace_3(venn_labels)
    elif len(data_dicts) == 2:
        layout = get_layout_2()
        trace = get_trace_2(venn_labels)
    else:
        raise ValueError(f'Venn diagram is not supported')

    fig = {
        'data': [trace],
        'layout': layout,
    }

    save_figure(f'{save_path}/venn', fig)

    return save_dicts