from paper.routines.infrastructure.path import get_data_path
from paper.routines.infrastructure.load.table import load_table_dict_xlsx
import numpy as np
import collections
from paper.routines.infrastructure.save.table import save_table_dict_xlsx
from paper.routines.routines import get_genes
from paper.routines.data.data_dicts import get_sets
from paper.routines.plot.venn import get_layout_2, get_layout_3, get_layout_4, get_trace_2, get_trace_3, get_trace_4
from paper.routines.infrastructure.save.figure import save_figure
import plotly.io as pio
import os
from tqdm import tqdm
from paper.routines.plot.pdf import get_pdf_x_and_y
from paper.routines.plot.layout import get_layout
import plotly.graph_objs as go
import colorlover as cl
import plotly
from paper.routines.infrastructure.load.table import load_table_dict
import plotly.express as px


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
    genes_duplicates = [item for item, count in collections.Counter(ssar_genes_lehallier).items() if count > 1]
    genes_duplicates_str = {'id': [], 'gene': []}
    for gene in genes_duplicates:
        ids = gene_id[gene]
        for id in ids:
            genes_duplicates_str['id'].append(id)
            genes_duplicates_str['gene'].append(gene)
    save_table_dict_xlsx(f'{save_path}/duplicates_ssar', genes_duplicates_str)

    return ss_genes_lehallier, ar_genes_lehallier, ssar_genes_lehallier

def process_human_plasma_proteome(target_dict, proteomic_genes, save_path, aux_key='aux'):

    fn_exp = 'E:/YandexDisk/Work/pydnameth/human_plasma_proteome/GTEx'
    exp_dict = load_table_dict(fn_exp)
    for tissue in exp_dict:
        if tissue not in ['Name', 'Description']:
            exp_dict[tissue] = np.log10(np.asarray(exp_dict[tissue]) + 1e-4)

    genes = {}
    for dataset in target_dict:
        for key in target_dict[dataset]:
            if 'aux_' in key:
                aux_key = key
                break
        genes[dataset] = {'gene': get_genes(target_dict[dataset], aux_key)}

    genes['Proteomic'] = {'gene': proteomic_genes}

    for dataset in genes:
        tmp_key = 'gene'
        print(f'num genes in {dataset}: {len(genes[dataset][tmp_key])}')

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
        gtex_processing(exp_dict, sets[set_key], set_key, curr_save_path)

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
    elif len(genes) == 2:
        layout = get_layout_2()
        trace = get_trace_2(venn_labels)
    else:
        raise ValueError(f'Venn diagram is not supported')

    fig = {
        'data': [trace],
        'layout': layout,
    }

    save_figure(f'{save_path}/venn', fig)


def gtex_processing(exp_dict, genes, main_key, save_path):

    gene_id_dict = dict(zip(exp_dict['Description'], list(range(0, len(exp_dict['Description'])))))

    result_dict = {key: [] for key in exp_dict}
    for gene in genes:
        if gene in gene_id_dict:
            row_id = gene_id_dict[gene]
            for key in result_dict:
                result_dict[key].append(exp_dict[key][row_id])

    save_table_dict_xlsx(f'{save_path}/{main_key}_expression', result_dict)

    target_keys = ['Whole Blood', 'Liver', 'Brain - Frontal Cortex (BA9)']
    plot_data = []
    for t_id, tissue in enumerate(target_keys):
        if len(result_dict[tissue]) > 0:
            xs, ys = get_pdf_x_and_y(result_dict[tissue], num_bins=50)
            color = cl.scales['8']['qual']['Set1'][t_id]
            coordinates = color[4:-1].split(',')
            color_border = 'rgba(' + ','.join(coordinates) + ',' + str(0.8) + ')'
            scatter = go.Scatter(
                x=xs,
                y=ys,
                name=tissue,
                mode='lines',
                line=dict(
                    width=4,
                    color=color_border
                ),
                showlegend=True
            )
            plot_data.append(scatter)
    layout = get_layout('$log_{2}GTEX$', 'Probability density function')
    fn = f'{save_path}/{main_key}'
    figure = go.Figure(data=plot_data, layout=layout)
    plotly.offline.plot(figure, filename=f'{fn}.html', auto_open=False, show_link=True)
    pio.write_image(figure, f'{fn}.png')
    pio.write_image(figure, f'{fn}.pdf')

    traces = []
    base_order = []

    color_scales = [px.colors.sequential.Reds[2:-2], px.colors.sequential.Blues[2:-2], px.colors.sequential.Greens[2:-2]]
    for t_id, tissue in enumerate(target_keys):
        if len(result_dict[tissue]) > 0:
            target_genes = result_dict['Description']
            target_exp = result_dict[tissue]
            if t_id == 0:
                base_order = np.argsort(target_exp)[::-1]
            genes_sorted = list(np.array(target_genes)[base_order])
            exp_sorted = list(np.array(target_exp)[base_order])

            traces.append(
                go.Bar(
                    orientation='h',
                    name=tissue,
                    y=genes_sorted,
                    x=[x + 4 for x in exp_sorted],
                    base=-4,
                    marker=dict(
                        color=[x + 4 for x in exp_sorted],
                        colorscale=color_scales[t_id],
                        colorbar=dict(
                            showticklabels=False,
                            len=1,
                            x=1 + 0.1 * t_id,
                            title=dict(
                                text=tissue.replace(' ', '<br>'),
                                font=dict(
                                    size=12,
                                    color=color_scales[t_id][-1]
                                ),
                                side='right'
                            ),
                        ),
                        showscale=True
                    )
                )
            )

    layout = go.Layout(
        plot_bgcolor='rgba(233,233,233,0)',
        barmode='overlay',
        showlegend=False,
        autosize=False,
        margin=go.layout.Margin(
            l=10,
            r=10,
            b=10,
            t=10,
            pad=0
        ),
        height=15 * (len(base_order) + 1),
        width=1000,
        xaxis=dict(
            gridcolor='rgb(100, 100, 100)',
            #gridwidth=0.01,
            mirror=True,
            linecolor='black',
            title='$log_{10}GTEX$',
            autorange=False,
            range=[-4, 5],
            showgrid=False,
            showline=True,
            titlefont=dict(
                family='Arial',
                size=30,
                color='black'
            ),
            showticklabels=True,
            tickangle=0,
            tickfont=dict(
                family='Arial',
                size=15,
                color='black'
            ),
            exponentformat='e',
            showexponent='all',
        ),
        yaxis=dict(
            gridcolor='rgb(100, 100, 100)',
            mirror=True,
            linecolor='black',
            autorange=True,
            showgrid=False,
            showline=True,
            tickangle=0,
            titlefont=dict(
                family='Arial',
                size=10,
                color='black'
            ),
            showticklabels=True,
            tickfont=dict(
                family='Arial',
                size=10,
                color='black'
            ),
            exponentformat='e',
            showexponent='all',
        ),
    )

    traces = traces[::-1]

    fn = f'{save_path}/{main_key}_combo'
    fig = go.Figure(data=traces, layout=layout)
    fig.update_layout(barmode='group')
    plotly.offline.plot(fig, filename=fn + '.html', auto_open=False, show_link=True)
    pio.write_image(fig, fn + '.png')
    pio.write_image(fig, fn + '.pdf')
