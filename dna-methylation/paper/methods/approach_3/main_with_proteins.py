import itertools
import numpy as np
import copy
from tqdm import tqdm
import os
from paper.routines.infrastructure.path import get_data_path
from paper.routines.infrastructure.load.table import load_table_dict_xlsx, load_table_dict_pkl
from paper.methods.approach_4.functions.minus_log_pvals_figure import minus_log_pvals_figure
from paper.routines.infrastructure.save.table import save_table_dict_xlsx
from paper.routines.plot.venn import get_layout_3, get_layout_4, get_trace_3, get_trace_4
from paper.routines.infrastructure.save.figure import save_figure
from paper.routines.routines import get_genes
import collections


minus_log_pval_percentile_lim = 99
pval_percentile_lim = 100 - minus_log_pval_percentile_lim
pval_lim = 0.05

data_type = 'residuals'
datasets = ['GSE87571', 'liver']
hashes = ['865f1a1aee2c567b7b839ac910801baf', '81f11bc49cb451091c552dce079bb478']
ss_key = 'ss'
ar_key = 'ar'
hashes_groups = [{ss_key: 'bb504d51', ar_key: '035a771b'}, {ss_key: 'ded0cd22', ar_key: 'b1f058b7'}]
cpg_key = 'item'
pval_key = 'p_value_fdr_bh'

annotations_keys = ['CHR', 'MAPINFO', 'UCSC_REFGENE_NAME', 'UCSC_REFGENE_GROUP', 'RELATION_TO_UCSC_CPG_ISLAND']
papers_keys = ['inoshita', 'singmann', 'yousefi']

save_path = f'{get_data_path()}/approaches/approach_3_with_proteomic'

ss_all_passed = {}
ar_all_passed = {}
ssar_all_passed = {}

pvals = {}
pvals_percentiles = {}

for ds_id, dataset in enumerate(datasets):
    curr_load_path = f'{get_data_path()}/{dataset}/{data_type}/table/aggregator/{hashes[ds_id]}'
    curr_save_path = f'{save_path}'

    if os.path.isfile(f'{curr_save_path}/{dataset}_ss.xlsx') \
            and os.path.isfile(f'{curr_save_path}/{dataset}_ar.xlsx') \
            and os.path.isfile(f'{curr_save_path}/{dataset}_ssar.xlsx') \
            and os.path.isfile(f'{curr_save_path}/{dataset}_pvals.xlsx') \
            and os.path.isfile(f'{curr_save_path}/{dataset}_pvals_percentiles.xlsx'):

        ss_passed = load_table_dict_xlsx(f'{curr_save_path}/{dataset}_ss.xlsx')
        ar_passed = load_table_dict_xlsx(f'{curr_save_path}/{dataset}_ar.xlsx')
        ssar_passed = load_table_dict_xlsx(f'{curr_save_path}/{dataset}_ssar.xlsx')
        pvals_curr = load_table_dict_xlsx(f'{curr_save_path}/{dataset}_pvals.xlsx')
        pvals_percentiles_curr = load_table_dict_xlsx(f'{curr_save_path}/{dataset}_pvals_percentiles.xlsx')

    else:
        data_dict = load_table_dict_pkl(f'{curr_load_path}/default.pkl')

        ss_passed = {}
        ar_passed = {}
        ssar_passed = {}
        for key in data_dict:
            ss_passed[key] = []
            ar_passed[key] = []
            ssar_passed[key] = []

        num_cpgs = len(data_dict[cpg_key])

        pval_ss = data_dict[f'{pval_key}_{hashes_groups[ds_id][ss_key]}']
        pval_ar = data_dict[f'{pval_key}_{hashes_groups[ds_id][ar_key]}']
        pval_ss_percentile = np.percentile(pval_ss, pval_percentile_lim)
        pval_ar_percentile = np.percentile(pval_ar, pval_percentile_lim)
        print(f'{dataset} persentile {ss_key}: {pval_ss_percentile}')
        print(f'{dataset} persentile {ar_key}: {pval_ar_percentile}')

        minus_log_pval_ss = -np.log10(pval_ss)
        minus_log_pval_ar = -np.log10(pval_ar)
        minus_log_pval_ss_percentile = np.percentile(minus_log_pval_ss, minus_log_pval_percentile_lim)
        minus_log_pval_ar_percentile = np.percentile(minus_log_pval_ar, minus_log_pval_percentile_lim)

        pvals_curr = {ss_key: minus_log_pval_ss, ar_key: minus_log_pval_ar}
        pvals_percentiles_curr = {ss_key: [minus_log_pval_ss_percentile], ar_key: [minus_log_pval_ar_percentile]}

        pvals[dataset] = pvals_curr
        pvals_percentiles[dataset] = pvals_percentiles_curr

        pval_lim_ss = min(pval_lim, np.power(10.0, -minus_log_pval_ss_percentile))
        pval_lim_ar = min(pval_lim, np.power(10.0, -minus_log_pval_ar_percentile))
        print(f'{dataset} pval lim {ss_key}: {pval_lim_ss}')
        print(f'{dataset} pval lim {ar_key}: {pval_lim_ar}')

        for cpg_id in tqdm(range(0, num_cpgs), desc=f'{dataset} processing'):

            if (data_dict[f'{pval_key}_{hashes_groups[ds_id][ss_key]}'][cpg_id] < pval_lim_ss):
                for key in data_dict:
                    ss_passed[key].append(data_dict[key][cpg_id])

            if (data_dict[f'{pval_key}_{hashes_groups[ds_id][ar_key]}'][cpg_id] < pval_lim_ar):
                for key in data_dict:
                    ar_passed[key].append(data_dict[key][cpg_id])

            if (data_dict[f'{pval_key}_{hashes_groups[ds_id][ss_key]}'][cpg_id] < pval_lim_ss) \
                    and (data_dict[f'{pval_key}_{hashes_groups[ds_id][ar_key]}'][cpg_id] < pval_lim_ar):
                for key in data_dict:
                    ssar_passed[key].append(data_dict[key][cpg_id])

        save_table_dict_xlsx(f'{curr_save_path}/{dataset}_ss', ss_passed)
        save_table_dict_xlsx(f'{curr_save_path}/{dataset}_ar', ar_passed)
        save_table_dict_xlsx(f'{curr_save_path}/{dataset}_ssar', ssar_passed)

        save_table_dict_xlsx(f'{curr_save_path}/{dataset}_pvals', pvals_curr)
        save_table_dict_xlsx(f'{curr_save_path}/{dataset}_pvals_percentiles', pvals_percentiles_curr)

    ss_all_passed[dataset] = ss_passed
    ar_all_passed[dataset] = ar_passed
    ssar_all_passed[dataset] = ssar_passed

    pvals[dataset] = pvals_curr
    pvals_percentiles[dataset] = pvals_percentiles_curr

minus_log_pvals_figure(pvals, pvals_percentiles, save_path)

lehallier_data_path = f'{get_data_path()}/human_plasma_proteome'
fn = lehallier_data_path + '/' + 'proteins_genes.xlsx'
proteins_genes_data_dict = load_table_dict_xlsx(fn)

id_gene = {}
gene_id = {}
suspect_rows = []
suspect_ids = []
for row_id in tqdm(range(0, len(proteins_genes_data_dict['ID']))):
    id = proteins_genes_data_dict['ID'][row_id]
    gene = proteins_genes_data_dict['EntrezGeneSymbol'][row_id]

    if gene in gene_id:
        gene_id[gene].append(id)
    else:
        gene_id[gene] = [id]

    if id in id_gene:
        suspect_rows.append(row_id)
        suspect_ids.append(id)
    if isinstance(gene, str):
        id_gene[id] = gene
    else:
        suspect_rows.append(row_id)
        suspect_ids.append(id)
suspect_rows = [x + 2 for x in suspect_rows]
np.savetxt(f'{save_path}/suspect_rows.txt', suspect_rows, fmt='%d')
np.savetxt(f'{save_path}/suspect_ids.txt', suspect_ids, fmt='%s')

fn = lehallier_data_path + '/' + 'age_sex.xlsx'
age_sex_data_dict = load_table_dict_xlsx(fn)
id_age_q = {}
id_sex_q = {}

for row_id in range(0, len(age_sex_data_dict['ID'])):
    id = age_sex_data_dict['ID'][row_id]
    age_q = age_sex_data_dict['q.Age'][row_id]
    sex_q = age_sex_data_dict['q.Sex'][row_id]

    id_age_q[id] = age_q
    id_sex_q[id] = sex_q

ar_genes_lehallier = []
ss_genes_lehallier = []
ssar_genes_lehallier = []
for id, gene in id_gene.items():
    if id_age_q[id] < 0.05:
        ar_genes_lehallier.append(gene)
    if id_sex_q[id] < 0.05:
        ss_genes_lehallier.append(gene)
    if id_age_q[id] < 0.05 and id_sex_q[id] < 0.05:
        ssar_genes_lehallier.append(gene)

print(f'Number of sex-specific (SS) genes in Lehallier, et. al.: {len(ss_genes_lehallier)}')
print(f'Number of unique sex-specific (SS) genes in Lehallier, et. al.: {len(set(ss_genes_lehallier))}')
genes_duplicates = [item for item, count in collections.Counter(ss_genes_lehallier).items() if count > 1]
genes_duplicates_str = {'id':[], 'gene':[]}
for gene in genes_duplicates:
    ids = gene_id[gene]
    for id in ids:
        genes_duplicates_str['id'].append(id)
        genes_duplicates_str['gene'].append(gene)
save_table_dict_xlsx(f'{save_path}/duplicates_ss', genes_duplicates_str)

print(f'Number of age-related (ar) genes in Lehallier, et. al.: {len(ar_genes_lehallier)}')
print(f'Number of unique age-related (ar) genes in Lehallier, et. al.: {len(set(ar_genes_lehallier))}')
genes_duplicates = [item for item, count in collections.Counter(ar_genes_lehallier).items() if count > 1]
genes_duplicates_str = {'id':[], 'gene':[]}
for gene in genes_duplicates:
    ids = gene_id[gene]
    for id in ids:
        genes_duplicates_str['id'].append(id)
        genes_duplicates_str['gene'].append(gene)
save_table_dict_xlsx(f'{save_path}/duplicates_ar', genes_duplicates_str)

print(f'Number of sex-specific age-related (ssae) genes in Lehallier, et. al.: {len(ssar_genes_lehallier)}')
print(f'Number of unique sex-specific age-related (ssae) genes in Lehallier, et. al.: {len(set(ssar_genes_lehallier))}')
genes_duplicates = [item for item, count in collections.Counter(ar_genes_lehallier).items() if count > 1]
genes_duplicates_str = {'id':[], 'gene':[]}
for gene in genes_duplicates:
    ids = gene_id[gene]
    for id in ids:
        genes_duplicates_str['id'].append(id)
        genes_duplicates_str['gene'].append(gene)
save_table_dict_xlsx(f'{save_path}/duplicates_ssar', genes_duplicates_str)

ways = ['ss', 'ar', 'ssar']

datasets += ['Proteomic']

for way in ways:

    if way == 'ss':
        target_dict = ss_all_passed
        proteomic_genes = ss_genes_lehallier
    elif way == 'ar':
        target_dict = ar_all_passed
        proteomic_genes = ar_genes_lehallier
    else:
        target_dict = ssar_all_passed
        proteomic_genes = ssar_genes_lehallier

    genes = {}
    for dataset in datasets:
        if dataset != 'Proteomic':
            genes[dataset] = get_genes(target_dict[dataset])
            print(f'{dataset} {way} number of genes: {len(genes[dataset])}')
        else:
            genes['Proteomic'] = proteomic_genes

    datasets_ids = list(range(0, len(datasets)))
    keys_ordered = copy.deepcopy(datasets)
    sets = {}
    checking = {}

    for dataset in datasets:
        sets[dataset] = set(genes[dataset])
        checking[dataset] = 0

    for L in range(2, len(datasets) + 1):
        for subset in itertools.combinations(datasets_ids, L):

            curr_ids = list(subset)

            curr_key_raw = np.sort(np.array(datasets)[np.array(curr_ids)])
            curr_key = '_'.join(list(curr_key_raw))

            if curr_key not in sets:

                cur_intersection = set(genes[datasets[curr_ids[0]]])
                for id in curr_ids[1::]:
                    cur_intersection = cur_intersection.intersection(set(genes[datasets[id]]))
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

    for dataset in datasets:
        if checking[dataset] != len(set(genes[dataset])):
            raise ValueError('Error in venn data creating')

    curr_save_path = f'{save_path}/intersection/{way}'
    if not os.path.exists(curr_save_path):
        os.makedirs(curr_save_path)

    for set_key in sets:
        save_dict = {}
        for metrics_key in ['gene']:
            save_dict[metrics_key] = []
        for i in sets[set_key]:
            save_dict['gene'].append(i)
        save_table_dict_xlsx(f'{curr_save_path}/{set_key}', save_dict)

    curr_save_path = f'{save_path}/intersection_with_difference/{way}'
    if not os.path.exists(curr_save_path):
        os.makedirs(curr_save_path)

    venn_labels = []
    for set_key in sets_with_difference:

        save_dict = {}
        for metrics_key in ['gene']:
            save_dict[metrics_key] = []
        for i in sets_with_difference[set_key]:
            save_dict['gene'].append(i)
        save_table_dict_xlsx(f'{curr_save_path}/{set_key}', save_dict)

        curr_labels = set_key.split('_') + [str(len(sets_with_difference[set_key]))]
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

    save_figure(f'{curr_save_path}/{keys_ordered[0]}', fig)
