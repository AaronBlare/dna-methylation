from routines.limma.annotations.load import load_annotations_dict
from routines.limma.annotations.subset import subset_annotations
from routines.limma.annotations.annotations import Annotations
from routines.limma.annotations.excluded import load_excluded
from routines.limma.annotations.add_info import add_info_to_dict
from paper.routines.infrastructure.load.table import load_table_dict_xlsx, load_table_dict_pkl
from paper.routines.infrastructure.save.table import save_table_dict_xlsx, save_table_dict_pkl
import os.path
from tqdm import tqdm
from paper.routines.plot.pdf import get_pdf_x_and_y
from paper.routines.plot.layout import get_layout
import plotly.graph_objs as go
import colorlover as cl
import numpy as np
import plotly

path = 'E:/YandexDisk/Work/pydnameth/limma'

datasets = ['GSE87571', 'GSE74193', 'liver']
data_type = 'm'

annotations = Annotations(
    name='annotations',
    type='450k',
    exclude='bad_cpgs',
    select_dict={
        'CHR': ['-X', '-Y']
    }
)

dataset_path_dict = {
    'GSE87571': 'E:/YandexDisk/Work/pydnameth/GSE87571',
    'GSE74193': 'E:/YandexDisk/Work/pydnameth/tissues/brain(DLPFC)/GSE74193',
    'liver': 'E:/YandexDisk/Work/pydnameth/liver'
}

values = {}
labels = {}
all_data = {}
xs = {}
ys = {}
metrics = []
for dataset in datasets:

    target_fn = f'{path}/{dataset}_{data_type}_filtered.pkl'
    if os.path.isfile(target_fn):
        filtered = load_table_dict_pkl(target_fn)
    else:
        ds_path = dataset_path_dict[dataset]
        annotations_dict = load_annotations_dict(f'{ds_path}/annotations')
        excluded = load_excluded(f'{ds_path}/bad_cpgs')
        subset_path = f'{path}/{dataset}'
        if not os.path.exists(subset_path):
            os.makedirs(subset_path)
        subset = subset_annotations(annotations, annotations_dict, excluded, subset_path)

        cpg_list = subset['cpg_list']
        cpg_gene_dict = subset['cpg_gene_dict']
        cpg_bop_dict = subset['cpg_bop_dict']
        gene_cpg_dict = subset['gene_cpg_dict']
        gene_bop_dict = subset['gene_bop_dict']
        bop_cpg_dict = subset['bop_cpg_dict']
        bop_gene_dict = subset['bop_gene_dict']
        cpg_map_info_dict = subset['cpg_map_info_dict']

        cpg_dict = { x : 0 for x in cpg_list }

        table_dict = load_table_dict_xlsx(f'{path}/{dataset}_{data_type}.xlsx')

        filtered = { x : [] for x in table_dict.keys() }
        for cpg_id, cpg in tqdm(enumerate(table_dict['CpG'])):
            if cpg in cpg_dict:
                for key in table_dict:
                    filtered[key].append(table_dict[key][cpg_id])

        metrics = list(filtered.keys())[1::]

        filtered = add_info_to_dict(filtered)

        save_table_dict_xlsx(f'{path}/{dataset}_{data_type}_filtered', filtered)
        save_table_dict_pkl(f'{path}/{dataset}_{data_type}_filtered', filtered)

    all_data[dataset] = filtered

    transforms = { x : 'lin' for x in metrics }

    values[dataset] = {}
    xs[dataset] = {}
    ys[dataset] = {}
    for key in metrics:
        if 'P.Val' in key:
            values[dataset][key] = -np.log10(np.asarray(filtered[key])[np.nonzero(filtered[key])])
            labels[key] = f'-lоg({key})'
        else:
            values[dataset][key] = np.asarray(filtered[key])
            labels[key] = key

        xs[dataset][key], ys[dataset][key] = get_pdf_x_and_y(values[dataset][key])

for key in metrics:

    plot_data = []
    for ds_id, dataset in enumerate(datasets):

        color = cl.scales['8']['qual']['Set1'][ds_id]
        coordinates = color[4:-1].split(',')
        color_border = 'rgba(' + ','.join(coordinates) + ',' + str(0.8) + ')'

        scatter = go.Scatter(
            x=xs[dataset][key],
            y=ys[dataset][key],
            name=dataset,
            mode='lines',
            line=dict(
                width=4,
                color=color_border
            ),
            showlegend=True
        )
        plot_data.append(scatter)

    layout = get_layout(labels[key], 'Probability density function')

    fn = f'{path}/figures/{key}'
    figure = go.Figure(data=plot_data, layout=layout)
    plotly.offline.plot(figure, filename=f'{fn}.html', auto_open=False, show_link=True)
    if 'P.Val' in key:
        figure.update_xaxes(range=[0, 20])
    plotly.io.write_image(figure, f'{fn}.png')
    plotly.io.write_image(figure, f'{fn}.pdf')


