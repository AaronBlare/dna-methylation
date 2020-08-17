from paper.routines.infrastructure.load.table import load_table_dict_xlsx
from paper.routines.infrastructure.save.table import save_table_dict_xlsx
from paper.routines.infrastructure.load.annotations import load_annotations_dict
from paper.methods.fisher.routines import perform_fisher, odds_ratio_plot
from collections import defaultdict
import numpy as np
import os


save_path = 'E:/YandexDisk/Work/pydnameth/approaches/approach_4/residuals/fisher'

global_fn = 'E:/YandexDisk/Work/pydnameth/approaches/approach_4/residuals/metal/direction_q_f_common.xlsx'
global_dict = load_table_dict_xlsx(global_fn)
global_probe_key = 'MarkerName'

target_fn = "E:/YandexDisk/Work/pydnameth/draft/fixes/materials_and_methods/update_4_bonferroni/saVMPs_males.xlsx"
target_dict = load_table_dict_xlsx(target_fn)
target_probe_key = 'CpG'

annotations_dict = load_annotations_dict()

target_variables = ['RELATION_TO_UCSC_CPG_ISLAND', 'CHR', 'UCSC_REFGENE_GROUP']
orders = {
    'RELATION_TO_UCSC_CPG_ISLAND': ['S_Shelf', 'S_Shore', 'Island', 'N_Shore', 'N_Shelf', 'NA'],
    'CHR': ['CHR_' + str(i) for i in range(1, 23)],
    'UCSC_REFGENE_GROUP': ['TSS1500', 'TSS200', '5\'UTR', '1stExon', 'Body', '3\'UTR']
}


for var in target_variables:

    count_global = {}
    for probe in global_dict[global_probe_key]:
        opts = annotations_dict[var][probe].split(';')
        for opt in opts:
            if opt in count_global:
                count_global[opt] += 1
            else:
                count_global[opt] = 1
    global_num = np.sum(list(count_global.values()))

    count_target = {}
    for probe in target_dict[target_probe_key]:
        opts = annotations_dict[var][probe].split(';')
        for opt in opts:
            if opt in count_target:
                count_target[opt] += 1
            else:
                count_target[opt] = 1
    target_num = np.sum(list(count_target.values()))

    count_global_mod = {}
    count_target_mod = {}
    odds_ratios = {}
    p_values = {}
    for opt in count_target:

        if var == 'CHR':
            if opt != '':
                count_global_mod[f'CHR_{str(opt)}'] = count_global[opt]
                count_target_mod[f'CHR_{str(opt)}'] = count_target[opt]
                opt = f'CHR_{str(opt)}'
        else:
            if opt != '':
                count_global_mod[opt] = count_global[opt]
                count_target_mod[opt] = count_target[opt]

        if opt == '':
            count_global_mod['NA'] = count_global[opt]
            count_target_mod['NA'] = count_target[opt]
            opt = 'NA'

        odds_ratio, p_value = perform_fisher(count_target_mod[opt], count_global_mod[opt], target_num, global_num)
        odds_ratios[opt] = odds_ratio
        p_values[opt] = p_value

    res_table_dict = defaultdict(list)
    for opt in orders[var]:
        res_table_dict[var].append(opt)
        res_table_dict['number of probes'].append(count_target_mod[opt])
        res_table_dict['total number of probes'].append(count_global_mod[opt])
        res_table_dict['p-value'].append(p_values[opt])
        res_table_dict['odds ratio'].append(odds_ratios[opt])

    if not os.path.exists(save_path):
        os.makedirs(save_path)
    save_table_dict_xlsx(f'{save_path}/{var}', res_table_dict)

    x_data = res_table_dict[var]
    y_data = list(map(float, res_table_dict['odds ratio']))

    odds_ratio_plot(x_data, y_data, f'{save_path}/{var}')
