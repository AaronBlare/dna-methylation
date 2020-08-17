from paper.routines.infrastructure.load.table import *
from paper.routines.data.human_plasma_proteome import *
from statsmodels.stats.multitest import multipletests
import numpy as np


def metal_preprocess(path, datasets, targets, suffix, is_rewrite=True):

    cpgs_set = set()

    for dataset in datasets:
        fn = path + f'/{dataset}'
        data_dict = load_table_dict(fn)
        if len(cpgs_set) != 0:
            cpgs_set.intersection_update(set(data_dict['item']))
        else:
            cpgs_set = set(data_dict['item'])
        target = data_dict['item']
        print(f'{dataset} num cpgs: {len(target)}')

    cpgs_dict = dict.fromkeys(cpgs_set)

    print(f'num_common cpgs: {len(cpgs_dict)}')

    for target in targets:
        fn = path + f'/{target}'
        data_dict = load_table_dict(fn)
        new_dict = {key: [] for key in data_dict}
        for cpg_id, cpg in enumerate(data_dict['MarkerName']):
            if cpg in cpgs_dict:
                for key in data_dict:
                    new_dict[key].append(data_dict[key][cpg_id])
        fn = path + f'/{target}_{suffix}'
        save_table_dict_xlsx(fn, new_dict, is_rewrite)


def metal_process(metal_type, pval_perc, path):

    fn = path + f'/{metal_type}'
    data_dict = load_table_dict(fn)

    reject, pvals_corr, alphacSidak, alphacBonf = multipletests(
        data_dict['P-value'],
        0.05,
        method='fdr_bh'
    )
    data_dict['p_value_fdr_bh'] = pvals_corr

    reject, pvals_corr, alphacSidak, alphacBonf = multipletests(
        data_dict['P-value'],
        0.05,
        method='bonferroni'
    )
    data_dict['p_value_fdr_bf'] = pvals_corr

    pvals = np.array(data_dict['p_value_fdr_bf'])
    directions = data_dict['Direction']
    #pvals_percentile = np.percentile(pvals, pval_perc)
    pvals_percentile = 0.01
    print(f'{metal_type} percentile: {pvals_percentile}')
    print(f'{metal_type} less 0.01: {np.count_nonzero(pvals_corr < 0.01)}')
    print(f'{metal_type} less 0.001: {np.count_nonzero(pvals_corr < 0.001)}')

    pvals_mod = -np.log10(pvals[np.nonzero(pvals)])
    xs, ys = get_pdf_x_and_y(pvals_mod)

    color = cl.scales['8']['qual']['Set1'][0]
    coordinates = color[4:-1].split(',')
    color_border = 'rgba(' + ','.join(coordinates) + ',' + str(0.8) + ')'

    y_max = 1.15 * max(ys)
    plot_data = []
    scatter = go.Scatter(
        x=xs,
        y=ys,
        name=metal_type,
        mode='lines',
        line=dict(
            width=4,
            color=color_border
        ),
        showlegend=True
    )
    plot_data.append(scatter)

    scatter = go.Scatter(
        x=[-np.log10(pvals_percentile)] * 2,
        y=[0, y_max],
        mode='lines',
        line=dict(
            width=4,
            color=color_border,
            dash='dot'
        ),
        showlegend=False
    )
    plot_data.append(scatter)

    layout = get_layout('$-log_{10}({pvalue})$', 'Probability density function')

    fn = f'{path}/{metal_type}'
    figure = go.Figure(data=plot_data, layout=layout)
    figure.update_xaxes(range=[min(xs), 1.3 * max(xs)])
    figure.update_yaxes(range=[0, y_max])
    plotly.offline.plot(figure, filename=f'{fn}.html', auto_open=False, show_link=True)
    plotly.io.write_image(figure, f'{fn}.png')
    plotly.io.write_image(figure, f'{fn}.pdf')

    data_dict_filtered = dict.fromkeys(data_dict.keys())
    for key in data_dict_filtered:
        data_dict_filtered[key] = []

    for cpg_id in tqdm(range(0, len(data_dict['MarkerName'])), desc=f'{metal_type} processing'):

        pval = pvals[cpg_id]

        direction = directions[cpg_id]

        if pval < pvals_percentile:
            if '?' in direction or len(set(list(direction))) == 1:
                for key in data_dict:
                    data_dict_filtered[key].append(data_dict[key][cpg_id])

    return data_dict_filtered