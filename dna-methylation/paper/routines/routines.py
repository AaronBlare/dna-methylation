def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def get_genes(data_dict, key='aux'):
    genes_raw = data_dict[key]

    genes_list = []
    for gene_raw in genes_raw:
        if isinstance(gene_raw, str):
            if gene_raw != '':
                curr_genes = gene_raw.split(';')
                genes_list += curr_genes

    print(f'number of cpgs: {len(genes_raw)}')
    print(f'number of genes: {len(list(set(genes_list)))}')

    return list(set(genes_list))