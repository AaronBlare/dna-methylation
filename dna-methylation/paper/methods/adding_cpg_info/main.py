from tqdm import tqdm
from paper.routines.infrastructure.path import get_data_path
from paper.routines.infrastructure.load.table import load_table_dict_xlsx
from paper.routines.infrastructure.load.annotations import load_annotations_dict
from paper.routines.infrastructure.load.papers import load_papers_dict
from paper.routines.infrastructure.save.table import save_table_dict_xlsx

method = 'polygon'
data_type = 'residuals'
version = 'v6'
dataset = 'GSE55763'
cpg_key = 'item'

annotations_keys = ['CHR', 'MAPINFO', 'UCSC_REFGENE_NAME', 'UCSC_REFGENE_GROUP', 'RELATION_TO_UCSC_CPG_ISLAND']
papers_keys = ['inoshita', 'singmann', 'yousefi']

path = get_data_path() + '/draft/tables/' + method + '/' + data_type + '/' + version

data_dicts_passed = {}
cpgs_dicts_passed = {}
R2s = {}
R2_percentiles = {}

data_dict = load_table_dict_xlsx(f'{path}/{dataset}.xlsx')

for key in annotations_keys:
    data_dict[key] = []
for key in papers_keys:
    data_dict[key] = []

annotations_dict = load_annotations_dict()
papers_dict = load_papers_dict()

for cpg in tqdm(data_dict[cpg_key], desc=f'intersection processing'):
    for key in annotations_keys:
        data_dict[key].append(annotations_dict[key][cpg])

    for paper_key in papers_keys:
        if cpg in papers_dict[paper_key]:
            data_dict[paper_key].append(1)
        else:
            data_dict[paper_key].append(0)

save_table_dict_xlsx(f'{path}/{data_type}_{dataset}_with_added_info', data_dict)
