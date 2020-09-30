import GEOparse
from data.routines.routines import is_float
from data.infrastructure.path import get_data_path, make_dir
from data.infrastructure.load.table import load_table_dict_xlsx, load_table_dict_pkl
from data.infrastructure.save.table import save_table_dict_pkl, save_table_dict_xlsx
import os
from tqdm import tqdm
import re
import numpy as np
from distutils.dir_util import copy_tree


def split_words(text):
    rgx = re.compile(r"((?:(?<!'|\w)(?:\w-?'?)+(?<!-))|(?:(?<='|\w)(?:\w-?'?)+(?=')))")
    return rgx.findall(text)

def only_words(words):
    passed_words = []
    for word in words:
        if not is_float(word):
            passed_words.append(word)
    return passed_words


GPL = '21145'
suffix = '22_09_20'

gsm_key = 'gsm'
gse_key = 'series_id'
source_key = 'source_name_ch1'
characteristics_key = 'characteristics_ch1'

fn_xlsx = f'{get_data_path()}/GPL{GPL}/GPL{GPL}_gsm_table_{suffix}.xlsx'
fn_pkl = f'{get_data_path()}/GPL{GPL}/GPL{GPL}_gsm_table_{suffix}.pkl'
if os.path.isfile(fn_pkl):
    gsm_raw_dict = load_table_dict_pkl(fn_pkl)
else:
    gsm_raw_dict = load_table_dict_xlsx(fn_xlsx)
    save_table_dict_pkl(fn_pkl, gsm_raw_dict)

gsms = gsm_raw_dict[gsm_key]

fn = f'{get_data_path()}/GPL{GPL}/bad_words.txt'
f = open(fn)
bad_words = set(f.read().splitlines())
f.close()

fn = f'{get_data_path()}/GPL{GPL}/target_chs.txt'
f = open(fn)
target_chs = set(f.read().splitlines())
f.close()

# data_dict_passed
fn_pkl = f'{get_data_path()}/GPL{GPL}/GPL{GPL}_gsm_dict.pkl'
if os.path.isfile(fn_pkl):
    gsm_dict = load_table_dict_pkl(fn_pkl)
else:
    gsm_dict = {}

    for key in tqdm(gsm_raw_dict, desc='gsm_dict processing'):
        gsm_dict[key] = {}
        for index, gsm in enumerate(gsms):
            gsm_dict[key][gsm] = gsm_raw_dict[key][index]

    save_table_dict_pkl(fn_pkl, gsm_dict)

# gse_gsms_dict
fn_pkl = f'{get_data_path()}/GPL{GPL}/gse_gsms_dict.pkl'
if os.path.isfile(fn_pkl):
    gse_gsms_dict = load_table_dict_pkl(fn_pkl)
else:
    gses = set()
    for gses_raw in gsm_raw_dict[gse_key]:
        gses_curr = gses_raw.split(',')
        for gse in gses_curr:
            gses.add(gse)
    gses = list(gses)

    gse_gsms_dict = {}
    for gse in gses:
        gse_gsms_dict[gse] = []

    for gsm in gsms:
        gses_raw = gsm_dict[gse_key][gsm]
        gses_curr = gses_raw.split(',')
        for gse in gses_curr:
            gse_gsms_dict[gse].append(gsm)

    save_table_dict_pkl(fn_pkl, gse_gsms_dict)

gses = sorted(gse_gsms_dict.keys(),  key=lambda s: len(gse_gsms_dict.get(s)), reverse=True)
with open(f'{get_data_path()}/GPL{GPL}/all_gses.txt', 'w') as f:
    for item in gses:
        f.write('%s\n' % item)

source_unique_words = set()
ch_unique_words = set()

gse_gsms_passed_dict = {}
gse_passed_dict = {}

for gse in tqdm(gses):

    path_all = f'{get_data_path()}/GPL{GPL}/all/{gse}'
    path_passed = f'{get_data_path()}/GPL{GPL}/passed/{gse}'
    make_dir(path_all)

    #if os.path.isfile(f'{path_tmp}/observables.xlsx'):
    #    continue

    gsms = gse_gsms_dict[gse]
    gsms_exist = []

    # Init characteristics dicts
    chs_keys = set()
    for gsm_id, gsm in enumerate(gsms):
        try:
            while True:
                try:
                    gsm_data = GEOparse.get_GEO(geo=gsm, destdir=f'{path_all}/gsms', include_data=False, how="")
                except ValueError:
                    continue
                except ConnectionError:
                    continue
                break
        except GEOparse.GEOparse.NoEntriesException:
            os.remove(f'{path_all}/gsms/{gsm}.txt')
            continue
        gsms_exist.append(gsm)
        chs_raw = gsm_data.metadata[characteristics_key]
        for ch in chs_raw:
            ch_split = ch.split(': ')
            chs_keys.update([ch_split[0]])

    gsms = gsms_exist
    gsms_passed = [True] * len(gsms)

    chs = {}
    chs['geo_accession'] = []
    ch_unique_words.update(chs_keys)
    for key in chs_keys:
        chs[key] = []

    for gsm_id, gsm in enumerate(gsms):

        gsm_data = GEOparse.get_GEO(geo=gsm, destdir=f'{path_all}/gsms', include_data=False, how="")

        gsm_is_passed = True

        chs['geo_accession'].append(gsm_data.metadata['geo_accession'][0])

        sources = gsm_data.metadata[source_key]
        for source in sources:
            if isinstance(source, str):
                sources_words = set(only_words(split_words(source.lower())))
                source_unique_words.update(sources_words)
                #if len(bad_words.intersection(sources_words)) > 0:
                #    gsm_is_passed = False

        chs_raw = gsm_data.metadata[characteristics_key]
        exist_chs = []
        for ch in chs_raw:
            ch_split = ch.split(': ')
            if ch_split[0] not in exist_chs:
                exist_chs.append(ch_split[0])
                ch_value = ': '.join(ch_split[1::])
                chs[ch_split[0]].append(ch_value)
                separate_words = set(only_words(split_words(ch_value.lower())))
                ch_unique_words.update(separate_words)
                #if len(bad_words.intersection(separate_words)) > 0:
                #    gsm_is_passed = False
        missed_chs = list(chs_keys.difference(exist_chs))
        for ch in missed_chs:
            chs[ch].append('NA')

        gsms_passed[gsm_id] = gsm_is_passed

    save_table_dict_xlsx(f'{path_all}/observables.xlsx', chs)

    chs_keys_set = set()
    for ch_key in chs_keys:
        separate_words = set(only_words(split_words(ch_key.lower())))
        chs_keys_set.update(separate_words)

    gse_gsms_passed_dict[gse] = gsms_passed
    if len(gsms_passed) == gsms_passed.count(False):
        gse_passed_dict[gse] = False
    else:
        all_here = True
        for target_ch in target_chs:
            curr_tar_chs = target_ch.split(' ')
            if len(chs_keys_set.intersection(set(curr_tar_chs))) == 0:
                all_here = False
                break
        if all_here:
            gse_passed_dict[gse] = True
        else:
            gse_passed_dict[gse] = False

    if gse_passed_dict[gse]:
        make_dir(path_passed)
        copy_tree(path_all, path_passed)

all_unique_words = list(source_unique_words.union(ch_unique_words))
with open(f'{get_data_path()}/GPL{GPL}/unique_words.txt', 'w') as f:
    for item in all_unique_words:
        f.write('%s\n' % item)
