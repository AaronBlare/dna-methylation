import os.path
import pickle
from routines.limma.annotations.check import global_check
import copy
import numpy as np


def subset_annotations(annotations, annotations_dict, excluded, aux_data_path):
    aux_data_fn = f'{aux_data_path}/aux_data.pkl'

    if os.path.isfile(aux_data_fn):
        f = open(aux_data_fn, 'rb')
        aux_data = pickle.load(f)
        f.close()
    else:
        aux_data = {}
        aux_data['cpg_list'] = []
        aux_data['cpg_gene_dict'] = {}
        aux_data['cpg_bop_dict'] = {}
        aux_data['gene_cpg_dict'] = {}
        aux_data['gene_bop_dict'] = {}
        aux_data['bop_cpg_dict'] = {}
        aux_data['bop_gene_dict'] = {}
        aux_data['cpg_map_info_dict'] = {}

        cpgs_all = annotations_dict['ID_REF']
        genes_all = annotations_dict['UCSC_REFGENE_NAME']
        bops_all = annotations_dict['BOP']
        map_infos_all = annotations_dict['MAPINFO']

        for index, cpg in enumerate(cpgs_all):

            if global_check(annotations, annotations_dict, excluded, index):

                cpg = cpgs_all[index][0]
                aux_data['cpg_list'].append(cpg)

                map_info = map_infos_all[index][0]
                if map_info == 'NA':
                    map_info = '0'
                aux_data['cpg_map_info_dict'][cpg] = int(map_info)

                genes = genes_all[index]
                if len(genes) > 0:
                    aux_data['cpg_gene_dict'][cpg] = genes
                    for gene in genes:
                        if gene in aux_data['gene_cpg_dict']:
                            aux_data['gene_cpg_dict'][gene].append(cpg)
                        else:
                            aux_data['gene_cpg_dict'][gene] = [cpg]

                bops = bops_all[index]
                if len(bops) > 0:
                    aux_data['cpg_bop_dict'][cpg] = bops
                    for bop in bops:
                        if bop in aux_data['bop_cpg_dict']:
                            aux_data['bop_cpg_dict'][bop].append(cpg)
                        else:
                            aux_data['bop_cpg_dict'][bop] = [cpg]

                if len(genes) > 0 and len(bops) > 0:
                    for gene in genes:
                        if gene in aux_data['gene_bop_dict']:
                            aux_data['gene_bop_dict'][gene] += bops
                        else:
                            aux_data['gene_bop_dict'][gene] = copy.deepcopy(bops)
                    for bop in bops:
                        if bop in aux_data['bop_gene_dict']:
                            aux_data['bop_gene_dict'][bop] += genes
                        else:
                            aux_data['bop_gene_dict'][bop] = copy.deepcopy(genes)

        # Sorting cpgs by map_info in gene dict
        for gene, cpgs in aux_data['gene_cpg_dict'].items():
            map_infos = []
            for cpg in cpgs:
                map_infos.append(int(aux_data['cpg_map_info_dict'][cpg]))
            order = np.argsort(map_infos)
            cpgs_sorted = list(np.array(cpgs)[order])
            aux_data['gene_cpg_dict'][gene] = cpgs_sorted

        # Sorting cpgs by map_info in bop dict
        for bop, cpgs in aux_data['bop_cpg_dict'].items():
            map_infos = []
            for cpg in cpgs:
                map_infos.append(int(aux_data['cpg_map_info_dict'][cpg]))
            order = np.argsort(map_infos)
            cpgs_sorted = list(np.array(cpgs)[order])
            aux_data['bop_cpg_dict'][bop] = cpgs_sorted

        f = open(aux_data_fn, 'wb')
        pickle.dump(aux_data, f, pickle.HIGHEST_PROTOCOL)
        f.close()

    return aux_data