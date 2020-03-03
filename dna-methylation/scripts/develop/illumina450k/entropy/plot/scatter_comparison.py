import pydnameth as pdm
import pandas as pd
import os.path

fn = 'scatter_comparison_rows.xlsx'
rows_dict = {}
if os.path.isfile(fn):
    df = pd.read_excel(fn)
    tmp_dict = df.to_dict()
    for key in tmp_dict:
        curr_dict = tmp_dict[key]
        rows_dict[key] = list(curr_dict.values())

fn = 'scatter_comparison_cols.xlsx'
cols_dict = {}
if os.path.isfile(fn):
    df = pd.read_excel(fn)
    tmp_dict = df.to_dict()
    for key in tmp_dict:
        curr_dict = tmp_dict[key]
        cols_dict[key] = list(curr_dict.values())

data_bases = cols_dict['data_bases']

data_list = []
annotations_list = []
attributes_list = []
observables_list = []
data_params_list = []

for data_base in data_bases:

    data = pdm.Data(
        path='',
        base=data_base
    )
    data_list.append(data)

    annotations = pdm.Annotations(
        name='annotations',
        type='450k',
        exclude='bad_cpgs',
        select_dict={
            'CHR': ['-X', '-Y']
        }
    )
    annotations_list.append(annotations)

    observables = pdm.Observables(
        name='observables',
        types={}
    )

    if data.base == 'GSE55763':
        obs = [
            {'gender': 'F', 'is_duplicate': '0', 'age': (35, 100)},
            {'gender': 'M', 'is_duplicate': '0', 'age': (35, 100)}
        ]

        data_params = {
            'data': 'betas_adj',
            'observables': ['age'],
            'cells': ['Bcell', 'CD4T', 'NK', 'CD8T', 'Gran']
        }

        cells = pdm.Cells(
            name='cells_horvath_calculator',
            types='any'
        )
    else:
        obs = [
            {'gender': 'F'},
            {'gender': 'M'}
        ]

        data_params = {
            'data': 'betas_adj',
            'observables': ['age'],
            'cells': ['B', 'CD4T', 'NK', 'CD8T', 'Gran']
        }

        cells = pdm.Cells(
            name='cells',
            types='any'
        )

    observables_list.append(obs)
    data_params_list.append(data_params)

    attributes = pdm.Attributes(
        target='age',
        observables=observables,
        cells=cells
    )
    attributes_list.append(attributes)

pdm.entropy_plot_scatter_comparison(
    data_list=data_list,
    annotations_list=annotations_list,
    attributes_list=attributes_list,
    observables_list=observables_list,
    data_params_list=data_params_list,
    rows_dict=rows_dict,
    cols_dict=cols_dict,
    method_params={
        'line': 'yes',
        'fit': 'none',
        'semi_window': 8,
        'box_b': 'Q5',
        'box_t': 'Q95',
        'legend_size': 1,
        'add': 'none'
    }
)
