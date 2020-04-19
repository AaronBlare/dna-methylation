from paper.routines.infrastructure.path import get_data_path
from paper.routines.infrastructure.load.table import load_table_dict_xlsx
from tqdm import tqdm
import numpy as np
import collections
from paper.routines.infrastructure.save.table import save_table_dict_xlsx
from paper.routines.routines import get_genes
from paper.routines.data.data_dicts import get_sets
from paper.routines.plot.venn import get_layout_3, get_layout_4, get_trace_3, get_trace_4
from paper.routines.infrastructure.save.figure import save_figure
import os


def get_human_plasma_proteome_dicts(save_path):

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

    print(f'Number of ss genes in Lehallier, et. al.: {len(ss_genes_lehallier)}')
    print(f'Number of UNIQUE ss genes in Lehallier, et. al.: {len(set(ss_genes_lehallier))}')
    genes_duplicates = [item for item, count in collections.Counter(ss_genes_lehallier).items() if count > 1]
    genes_duplicates_str = {'id': [], 'gene': []}
    for gene in genes_duplicates:
        ids = gene_id[gene]
        for id in ids:
            genes_duplicates_str['id'].append(id)
            genes_duplicates_str['gene'].append(gene)
    save_table_dict_xlsx(f'{save_path}/duplicates_ss', genes_duplicates_str)

    print(f'Number of ar genes in Lehallier, et. al.: {len(ar_genes_lehallier)}')
    print(f'Number of UNIQUE ar genes in Lehallier, et. al.: {len(set(ar_genes_lehallier))}')
    genes_duplicates = [item for item, count in collections.Counter(ar_genes_lehallier).items() if count > 1]
    genes_duplicates_str = {'id': [], 'gene': []}
    for gene in genes_duplicates:
        ids = gene_id[gene]
        for id in ids:
            genes_duplicates_str['id'].append(id)
            genes_duplicates_str['gene'].append(gene)
    save_table_dict_xlsx(f'{save_path}/duplicates_ar', genes_duplicates_str)

    print(f'Number of ssar genes in Lehallier, et. al.: {len(ssar_genes_lehallier)}')
    print(f'Number of UNIQUE ssar genes in Lehallier, et. al.: {len(set(ssar_genes_lehallier))}')
    genes_duplicates = [item for item, count in collections.Counter(ar_genes_lehallier).items() if count > 1]
    genes_duplicates_str = {'id': [], 'gene': []}
    for gene in genes_duplicates:
        ids = gene_id[gene]
        for id in ids:
            genes_duplicates_str['id'].append(id)
            genes_duplicates_str['gene'].append(gene)
    save_table_dict_xlsx(f'{save_path}/duplicates_ssar', genes_duplicates_str)

    return ss_genes_lehallier, ar_genes_lehallier, ssar_genes_lehallier

def process_human_plasma_proteome(target_dict, proteomic_genes, save_path):

    aux_key = 'aux'
    for key in target_dict[list(target_dict.keys())[0]]:
        if 'aux_' in key:
            aux_key = key
            break

    genes = {}
    for dataset in target_dict:
        genes[dataset] = {'gene': get_genes(target_dict[dataset], aux_key)}

    genes['Proteomic'] = {'gene': proteomic_genes}

    sets, sets_with_difference = get_sets(genes, item_key='gene')

    curr_save_path = f'{save_path}/intersection'
    if not os.path.exists(curr_save_path):
        os.makedirs(curr_save_path)
    for set_key in sets:
        save_dict = {}
        for metrics_key in ['gene']:
            save_dict[metrics_key] = []
        for i in sets[set_key]:
            save_dict['gene'].append(i)
        save_table_dict_xlsx(f'{curr_save_path}/{set_key}', save_dict)

    curr_save_path = f'{save_path}/intersection_with_difference'
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

    if len(genes) == 4:
        layout = get_layout_4()
        trace = get_trace_4(venn_labels)
    elif len(genes) == 3:
        layout = get_layout_3()
        trace = get_trace_3(venn_labels)
    else:
        raise ValueError(f'Venn diagram is not supported')

    fig = {
        'data': [trace],
        'layout': layout,
    }

    save_figure(f'{save_path}/venn', fig)
