from paper.routines.infrastructure.load.annotations import load_annotations_dict

def add_info_to_dict(data_dict, cpg_key='CpG'):

    annotations_keys = ['CHR', 'MAPINFO', 'UCSC_REFGENE_NAME', 'UCSC_REFGENE_GROUP', 'RELATION_TO_UCSC_CPG_ISLAND']
    annotations_dict = load_annotations_dict()

    for key in annotations_keys:
        data_dict[key] = []

    for cpg in data_dict[cpg_key]:
        for key in annotations_keys:
            data_dict[key].append(annotations_dict[key][cpg])

    return data_dict