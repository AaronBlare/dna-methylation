from paper.routines.data.human_plasma_proteome import *
from statsmodels.stats.multitest import multipletests
import copy


def metal_preprocess(path, datasets, targets, suffix):

    cpgs_set = set()

    for dataset in datasets:
        fn = path + f'/{dataset}.xlsx'
        data_dict = load_table_dict_xlsx(fn)
        if len(cpgs_set) != 0:
            cpgs_set.intersection_update(set(data_dict['item']))
        else:
            cpgs_set = set(data_dict['item'])
        target = data_dict['item']
        print(f'{dataset} num cpgs: {len(target)}')

    cpgs_dict = dict.fromkeys(cpgs_set)

    print(f'num_common cpgs: {len(cpgs_dict)}')

    for target in targets:
        fn = path + f'/{target}.xlsx'
        data_dict = load_table_dict_xlsx(fn)
        new_dict = {key: [] for key in data_dict}
        for cpg_id, cpg in enumerate(data_dict['MarkerName']):
            if cpg in cpgs_dict:
                for key in data_dict:
                    new_dict[key].append(data_dict[key][cpg_id])
        fn = path + f'/{target}_{suffix}'
        save_table_dict_xlsx(fn, new_dict)


def get_metal_dicts(path, types):

    metal_dicts = {}

    for metal_type in types:

        fn = path + f'/{metal_type}.xlsx'
        metal_dicts[metal_type] = load_table_dict_xlsx(fn)

        reject, pvals_corr, alphacSidak, alphacBonf = multipletests(
            metal_dicts[metal_type]['P-value'],
            0.05,
            #method='fdr_bh',
            method='bonferroni'
        )
        metal_dicts[metal_type]['p_value_fdr'] = pvals_corr

    return metal_dicts


def process_metal(data_dicts, metal_dicts, pval_perc, pval_null_lim, save_path):

    target_keys = ['item', 'p_value_f', 'p_value_m', 'dir_f', 'dir_m']
    for dataset in data_dicts:
        target_keys.append(f'type_f_{dataset}')
        target_keys.append(f'type_m_{dataset}')

    f_metal_dict = {key:[] for key in target_keys}
    m_metal_dict = copy.deepcopy(f_metal_dict)
    fm_metal_dict = copy.deepcopy(f_metal_dict)
    global_dict = copy.deepcopy(f_metal_dict)

    f_pvals = metal_dicts['direction_p_f_common']['p_value_fdr']
    m_pvals = metal_dicts['direction_p_m_common']['p_value_fdr']

    f_dirs = metal_dicts['direction_p_f_common']['Direction']
    m_dirs = metal_dicts['direction_p_m_common']['Direction']

    f_pvals_percentiles = np.percentile(f_pvals, [pval_perc, 100 - pval_perc])
    f_pvals_percentiles[0] = 0.01
    print(f'f percentile {pval_perc}: {f_pvals_percentiles[0]}')
    print(f'f percentile {100 - pval_perc}: {f_pvals_percentiles[1]}')

    m_pvals_percentiles = np.percentile(m_pvals, [pval_perc, 100 - pval_perc])
    m_pvals_percentiles[0] = 0.01
    print(f'm percentile {pval_perc}: {m_pvals_percentiles[0]}')
    print(f'm percentile {100 - pval_perc}: {m_pvals_percentiles[1]}')

    probes = metal_dicts['direction_p_f_common']['MarkerName']

    f_directions_dict = {}
    m_directions_dict = {}
    for dataset in data_dicts:
        f_directions_dict[dataset] = {}
        m_directions_dict[dataset] = {}
        cpgs = data_dicts[dataset]['item']
        types_f = data_dicts[dataset]['type_f']
        types_m = data_dicts[dataset]['type_m']
        for cpg_id in tqdm(range(0, len(data_dicts[dataset]['item'])), desc=f'{dataset} processing'):
            type_f = types_f[cpg_id]
            type_m = types_m[cpg_id]
            cpg = cpgs[cpg_id]
            f_directions_dict[dataset][cpg] = type_f
            m_directions_dict[dataset][cpg] = type_m

    for probe_id in tqdm(range(0, len(probes)), desc=f'metal processing'):

        probe = probes[probe_id]
        pval_f = f_pvals[probe_id]
        pval_m = m_pvals[probe_id]
        dir_f = f_dirs[probe_id]
        dir_m = m_dirs[probe_id]

        f_is_same_direction = False
        m_is_same_direction = False
        f_directions = []
        m_directions = []
        for dataset in data_dicts:
            if probe in f_directions_dict[dataset]:
                f_directions.append(f_directions_dict[dataset][probe])
            if probe in m_directions_dict[dataset]:
                m_directions.append(m_directions_dict[dataset][probe])

        if len(f_directions) == len(data_dicts.keys()) and len(set(f_directions)) == 1:
            f_is_same_direction = True
        if len(m_directions) == len(data_dicts.keys()) and len(set(m_directions)) == 1:
            m_is_same_direction = True

        if f_is_same_direction:

            if pval_f < f_pvals_percentiles[0] and pval_m > pval_null_lim:
                f_metal_dict['item'].append(probe)
                f_metal_dict['p_value_f'].append(pval_f)
                f_metal_dict['p_value_m'].append(pval_m)
                f_metal_dict['dir_f'].append(dir_f)
                f_metal_dict['dir_m'].append(dir_m)
                for dataset in data_dicts:
                    f_metal_dict[f'type_f_{dataset}'].append(f_directions_dict[dataset][probe])
                    f_metal_dict[f'type_m_{dataset}'].append(m_directions_dict[dataset][probe])

        if m_is_same_direction:

            if pval_m < m_pvals_percentiles[0] and pval_f > pval_null_lim:
                m_metal_dict['item'].append(probe)
                m_metal_dict['p_value_f'].append(pval_f)
                m_metal_dict['p_value_m'].append(pval_m)
                m_metal_dict['dir_f'].append(dir_f)
                m_metal_dict['dir_m'].append(dir_m)
                for dataset in data_dicts:
                    m_metal_dict[f'type_f_{dataset}'].append(f_directions_dict[dataset][probe])
                    m_metal_dict[f'type_m_{dataset}'].append(m_directions_dict[dataset][probe])

        if f_is_same_direction and m_is_same_direction:

            f_direction = list(set(f_directions))[0]
            m_direction = list(set(m_directions))[0]

            if pval_f < f_pvals_percentiles[0] and pval_m < m_pvals_percentiles[0] and f_direction != m_direction:
                fm_metal_dict['item'].append(probe)
                fm_metal_dict['p_value_f'].append(pval_f)
                fm_metal_dict['p_value_m'].append(pval_m)
                fm_metal_dict['dir_f'].append(dir_f)
                fm_metal_dict['dir_m'].append(dir_m)
                for dataset in data_dicts:
                    fm_metal_dict[f'type_f_{dataset}'].append(f_directions_dict[dataset][probe])
                    fm_metal_dict[f'type_m_{dataset}'].append(m_directions_dict[dataset][probe])

        global_dict['item'].append(probe)
        global_dict['p_value_f'].append(pval_f)
        global_dict['p_value_m'].append(pval_m)
        global_dict['dir_f'].append(dir_f)
        global_dict['dir_m'].append(dir_m)
        for dataset in data_dicts:
            global_dict[f'type_f_{dataset}'].append(f_directions_dict[dataset][probe])
            global_dict[f'type_m_{dataset}'].append(m_directions_dict[dataset][probe])

    return f_metal_dict, m_metal_dict, fm_metal_dict, global_dict
