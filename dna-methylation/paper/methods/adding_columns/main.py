from paper.routines.infrastructure.load.table import load_table_dict_by_key_xlsx, load_table_dict_xlsx
from paper.routines.infrastructure.save.table import save_table_dict_xlsx

# contrasts = ['Treatment', 'Simple', 'Sum', 'Diff']
# datasets = ['GSE40279', 'GSE87571', 'EPIC', 'GSE55763']
#
# for contrast in contrasts:
#     for dataset in datasets:
#
#         source_fn = f'E:/YandexDisk/Work/pydnameth/approaches/ancova/{contrast}/{dataset}.xlsx'
#         source_keys = ['x:category_pval', 'x:category']
#
#         target_fn = 'E:/YandexDisk/Work/pydnameth/draft/fixes/materials_and_methods/update_3_direction_for_ar_and_ss/supplementary_file_1_tmp.xlsx'
#         target_main_key = 'CpG'
#         target_keys = [f'interaction p-value ({dataset} {contrast})', f'interaction coeff ({dataset} {contrast})']

#contrasts = ['Treatment', 'Simple', 'Sum', 'Diff']

#for contrast in contrasts:


#source_fn = f'E:/YandexDisk/Work/pydnameth/approaches/ancova/{contrast}/direction_q.xlsx'
#source_keys = ['P-value', 'Direction']

#target_fn = 'E:/YandexDisk/Work/pydnameth/draft/fixes/materials_and_methods/update_3_direction_for_ar_and_ss/supplementary_file_1_tmp.xlsx'
#target_main_key = 'CpG'
#target_keys = [f'METAL interaction p-value ({contrast})', f'METAL interaction direction ({contrast})']

#save_fn = 'E:/YandexDisk/Work/pydnameth/draft/fixes/materials_and_methods/update_3_direction_for_ar_and_ss/supplementary_file_1_tmp'

datasets = ['GSE40279', 'GSE87571', 'EPIC', 'GSE55763']

for dataset in datasets:

    print(dataset)

    source_fn = f'E:/YandexDisk/Work/pydnameth/approaches/ancova/Treatment/{dataset}.xlsx'
    source_keys = ['x:category_pval', 'x:category']

    target_fn = 'E:/YandexDisk/Work/pydnameth/draft/fixes/materials_and_methods/update_4_bonferroni/ssDMPs_ext.xlsx'
    target_main_key = 'MarkerName'
    target_keys = [f'interaction p-value ({dataset})', f'interaction coeff ({dataset})']

    save_fn = 'E:/YandexDisk/Work/pydnameth/draft/fixes/materials_and_methods/update_4_bonferroni/ssDMPs_ext'

    source_dict = load_table_dict_by_key_xlsx(source_fn, 'item')
    target_dict = load_table_dict_xlsx(target_fn)

    for key in target_keys:
        target_dict[key] = []
    for item in target_dict[target_main_key]:
        for key_id, key  in enumerate(target_keys):
            if item in source_dict[source_keys[key_id]]:
                target_dict[key].append(source_dict[source_keys[key_id]][item])
            else:
                target_dict[key].append('NA')

    save_table_dict_xlsx(save_fn, target_dict)
