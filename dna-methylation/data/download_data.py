import GEOparse
from GEOparse.utils import download_from_url
from data.routines.routines import is_float
from data.infrastructure.path import get_data_path, make_dir
from data.infrastructure.load.table import load_table_dict_xlsx, load_table_dict_pkl
from data.infrastructure.save.table import save_table_dict_pkl, save_table_dict_xlsx, save_table_dict_csv
import os
import numpy as np
from tqdm import tqdm
import re
import gzip
import shutil
import ntpath
import pickle

na_values = ['', '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND', '1.#QNAN', '<NA>',
             'N/A', 'NA', 'NULL', 'NaN', 'n/a', 'nan', 'null', '-', '--']

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

target_dir = f'{get_data_path()}/GPL{GPL}/test_single'

fn_xlsx = f'{get_data_path()}/GPL{GPL}/GPL{GPL}_gsm_table_{suffix}.xlsx'
fn_pkl = f'{get_data_path()}/GPL{GPL}/GPL{GPL}_gsm_table_{suffix}.pkl'
if os.path.isfile(fn_pkl):
    gsm_raw_dict = load_table_dict_pkl(fn_pkl)
else:
    gsm_raw_dict = load_table_dict_xlsx(fn_xlsx)
    save_table_dict_pkl(fn_pkl, gsm_raw_dict)

gsms = gsm_raw_dict[gsm_key]

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


gses = [f.name for f in os.scandir(target_dir) if f.is_dir()]

gse_gsms_passed_dict = {}
gse_passed_dict = {}

for gse in tqdm(gses):

    path_data = f'{target_dir}/{gse}/raw_data'
    make_dir(path_data)

    gsms = gse_gsms_dict[gse]

    gsms_exist = []
    base_names = {}
    chs_keys = set()
    betas_dfs = {}
    is_beta_process = False
    cpgs = set()

    files_downloaded = set()
    for gsm_id, gsm in tqdm(enumerate(gsms), desc='data loading'):
        try:
            while True:
                try:
                    gsm_data = GEOparse.get_GEO(geo=gsm, destdir=f'{path_data}', include_data=True, how="", silent=True)
                    os.remove(f'{path_data}/{gsm}.txt')

                    # characteristics processing
                    gsms_exist.append(gsm)
                    chs_raw = gsm_data.metadata[characteristics_key]
                    for ch in chs_raw:
                        ch_split = ch.split(': ')
                        chs_keys.update([ch_split[0]])


                    tail = 'none'
                    if gsm_data.metadata['supplementary_file'][0] != 'NONE':
                        # raw signal downloading
                        for supp_file in gsm_data.metadata['supplementary_file']:
                            head, tail = ntpath.split(supp_file)
                            if tail[:-3] in files_downloaded:
                                raise ValueError('File duplication')
                            files_downloaded.add(tail[:-3])
                            if not os.path.exists( f'{path_data}/{tail[:-3]}'):
                                download_from_url(supp_file, f'{path_data}/{tail}')
                                with gzip.open( f'{path_data}/{tail}', 'rb') as f_in:
                                    with open( f'{path_data}/{tail[:-3]}', 'wb') as f_out:
                                        shutil.copyfileobj(f_in, f_out)
                                os.remove(f'{path_data}/{tail}')
                    else:
                        # beta-values downloading
                        gsm_data = GEOparse.get_GEO(geo=gsm, destdir=f'{path_data}', include_data=True, how="full")
                        os.remove(f'{path_data}/{gsm}.txt')
                        is_beta_process = True

                        betas_dfs[gsm] = gsm_data.table
                        cpgs.update(set(gsm_data.table['ID_REF']))

                    if tail == 'none':
                        base_names[gsm] = tail
                    else:
                        base_names[gsm] = os.path.splitext(tail)[0][0:-9]

                except ValueError:
                    continue
                except ConnectionError:
                    continue
                break
        except GEOparse.GEOparse.NoEntriesException:
            continue

    gsms = gsms_exist

    print(f'len(gsms_exist) = {len(gsms_exist)}')
    print(f'len(files_downloaded) = {len(files_downloaded)}')

    if is_beta_process:
        cpgs = list(cpgs)
        cpgs.sort()

        betas_dict = {}
        betas_missed_dict = {}
        betas_missed_dict['any'] = []
        betas_data = np.full((len(cpgs), len(gsms)), np.nan, dtype=np.float32)

        for cpg_id, cpg in enumerate(cpgs):
            betas_dict[cpg] = cpg_id

        for gsm_id, gsm in tqdm(enumerate(gsms), desc='data filling'):
            df = betas_dfs[gsm]
            curr_cpgs = df['ID_REF'].tolist()
            curr_betas = df['VALUE'].tolist()
            for cpg_id, cpg in enumerate(curr_cpgs):
                betas_data[betas_dict[cpg], gsm_id] = curr_betas[cpg_id]

        for cpg in tqdm(betas_dict, desc='missing filling'):
            row = betas_dict[cpg]
            betas = betas_data[row, :]
            missed_indexes = list(np.argwhere(np.isnan(betas)))
            betas_missed_dict[cpg] = missed_indexes

        f = open(f'{path_data}/betas_dict.pkl', 'wb')
        pickle.dump(betas_dict, f,  pickle.HIGHEST_PROTOCOL)
        f.close()

        f = open(f'{path_data}/betas_missed_dict.pkl', 'wb')
        pickle.dump(betas_missed_dict, f, pickle.HIGHEST_PROTOCOL)
        f.close()

        np.savez_compressed(f'{path_data}/betas.npz', data=betas_data)

    chs = {}
    chs['geo_accession'] = []
    chs['Basename'] = []
    chs['Array'] = []
    chs['Slide'] = []
    chs['Sample_Group'] = []
    for key in chs_keys:
        chs[key] = []

    for gsm_id, gsm in tqdm(enumerate(gsms), desc='data postprocess'):

        # characteristics processing
        chs['Basename'].append(base_names[gsm])
        pd_parts = base_names[gsm].split('_')
        chs['Array'].append(pd_parts[-1])
        chs['Slide'].append(pd_parts[-2])
        chs['Sample_Group'].append('C')
        try:
            while True:
                try:
                    gsm_data = GEOparse.get_GEO(geo=gsm, destdir=f'{path_data}', include_data=True, how="", silent=True)
                    os.remove(f'{path_data}/{gsm}.txt')
                except ValueError:
                    continue
                except ConnectionError:
                    continue
                break
        except GEOparse.GEOparse.NoEntriesException:
            continue

        chs['geo_accession'].append(gsm_data.metadata['geo_accession'][0])
        chs_raw = gsm_data.metadata[characteristics_key]
        exist_chs = []
        for ch in chs_raw:
            ch_split = ch.split(': ')
            if ch_split[0] not in exist_chs:
                exist_chs.append(ch_split[0])
                ch_value = ': '.join(ch_split[1::])
                chs[ch_split[0]].append(ch_value)
        missed_chs = list(chs_keys.difference(exist_chs))
        for ch in missed_chs:
            chs[ch].append('NA')

    save_table_dict_csv(f'{path_data}/observables', chs)
