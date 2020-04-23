from paper.routines.data.data_dicts import *
from paper.routines.data.approaches import *
from paper.methods.approach_3.filter import filter_data_dicts
from paper.routines.data.human_plasma_proteome import *


pval_perc = 5
pval_lim = 0.05
pval_prefix = 'p_value_fdr_bh'

main_key = 'GSE40279_GSE87571'

type = 'residuals'
names = ['GSE40279', 'GSE87571']
datasets = [Dataset(type, name) for name in names]

keys_save = [
    'item',
    'aux',
    'corr_coeff_ss',
    'p_value_ss',
    'p_value_fdr_bh_ss',
    'p_value_fdr_hb_ss',
    'corr_coeff_ar',
    'p_value_ar',
    'p_value_fdr_bh_ar',
    'p_value_fdr_hb_ar'
]

keys_load = {}
for dataset in datasets:
    keys_load[dataset.name] = [
        'item',
        'aux',
        f'corr_coeff_{get_ss_hash(dataset)}',
        f'p_value_{get_ss_hash(dataset)}',
        f'p_value_fdr_bh_{get_ss_hash(dataset)}',
        f'p_value_bonferroni_{get_ss_hash(dataset)}',
        f'corr_coeff_{get_ar_hash(dataset)}',
        f'p_value_{get_ar_hash(dataset)}',
        f'p_value_fdr_bh_{get_ar_hash(dataset)}',
        f'p_value_bonferroni_{get_ar_hash(dataset)}',
    ]

save_path = f'{get_data_path()}/approaches/approach_3/{type}'
if not os.path.exists(save_path):
    os.makedirs(save_path)
if not os.path.exists(f'{save_path}/ss'):
    os.makedirs(f'{save_path}/ss')
if not os.path.exists(f'{save_path}/ar'):
    os.makedirs(f'{save_path}/ar')
if not os.path.exists(f'{save_path}/ssar'):
    os.makedirs(f'{save_path}/ssar')

if not os.path.exists(f'{save_path}/proteome'):
    os.makedirs(f'{save_path}/proteome')
ss_genes_lehallier, ar_genes_lehallier, ssar_genes_lehallier = get_human_plasma_proteome_dicts(f'{save_path}/proteome')

data_dicts = get_data_dicts(datasets, 'aggregator', keys_load, keys_save, get_approach_3_hash)
ss_data_dicts, ar_data_dicts, ssar_data_dicts = filter_data_dicts(data_dicts, pval_prefix, pval_perc, save_path)

ss_result_dicts = process_intersections(ss_data_dicts, f'{save_path}/ss')
ar_result_dicts = process_intersections(ar_data_dicts, f'{save_path}/ar')
ssar_result_dicts = process_intersections(ssar_data_dicts, f'{save_path}/ssar')

if not os.path.exists(f'{save_path}/proteome/ss'):
    os.makedirs(f'{save_path}/proteome/ss')
ss_target_dict = {'Methylation': ss_result_dicts[main_key]}
process_human_plasma_proteome(ss_target_dict, ss_genes_lehallier, f'{save_path}/proteome/ss')

if not os.path.exists(f'{save_path}/proteome/ar'):
    os.makedirs(f'{save_path}/proteome/ar')
ar_target_dict = {'Methylation': ar_result_dicts[main_key]}
process_human_plasma_proteome(ar_target_dict, ar_genes_lehallier, f'{save_path}/proteome/ar')

if not os.path.exists(f'{save_path}/proteome/ssar'):
    os.makedirs(f'{save_path}/proteome/ssar')
ssar_target_dict = {'Methylation': ssar_result_dicts[main_key]}
process_human_plasma_proteome(ssar_target_dict, ssar_genes_lehallier, f'{save_path}/proteome/ssar')
