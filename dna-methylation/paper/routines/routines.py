def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def get_genes(data_dict, key='aux'):
    genes_raw = data_dict[key]
    print(f'number of cpgs: {len(genes_raw)}')

    genes_list = []
    for gene_raw in genes_raw:
        if isinstance(gene_raw, str):
            curr_genes = gene_raw.split(';')
            genes_list += curr_genes

    return list(set(genes_list))