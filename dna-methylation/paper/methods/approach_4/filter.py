import copy
from collections import defaultdict
from tqdm import tqdm
from paper.routines.plot.pdf import get_pdf_x_and_y
from paper.routines.plot.layout import get_layout
import plotly.graph_objs as go
import colorlover as cl
import plotly
import numpy as np


def filter_data_dicts(data_dicts, pval_perc, pval_null_lim, save_path):

    f_data_dicts = dict.fromkeys(data_dicts.keys())
    for dd in f_data_dicts:
        f_data_dicts[dd] = defaultdict(list)
    m_data_dicts = copy.deepcopy(f_data_dicts)
    fm_data_dicts = copy.deepcopy(f_data_dicts)

    f_xs = dict.fromkeys(data_dicts.keys())
    f_ys = dict.fromkeys(data_dicts.keys())

    m_xs = dict.fromkeys(data_dicts.keys())
    m_ys = dict.fromkeys(data_dicts.keys())

    f_percentiles = {}
    m_percentiles = {}

    for dataset in data_dicts:

        types_f = data_dicts[dataset][f'type_f']
        types_m = data_dicts[dataset][f'type_m']
        pvals_f = np.array(data_dicts[dataset][f'bp_f_pvalue_fdr_bh_f'])
        pvals_m = np.array(data_dicts[dataset][f'bp_f_pvalue_fdr_bh_m'])
        pval_f_percentile = min(np.percentile(pvals_f, pval_perc), 0.05)
        pval_m_percentile = min(np.percentile(pvals_m, pval_perc), 0.05)
        print(f'{dataset} f percentile: {pval_f_percentile}')
        print(f'{dataset} m percentile: {pval_m_percentile}')
        f_percentiles[dataset] = pval_f_percentile
        m_percentiles[dataset] = pval_m_percentile

        pvals_f_mod = -np.log10(pvals_f[np.nonzero(pvals_f)])
        f_xs[dataset], f_ys[dataset] = get_pdf_x_and_y(pvals_f_mod)
        pvals_m_mod = -np.log10(pvals_m[np.nonzero(pvals_m)])
        m_xs[dataset], m_ys[dataset] = get_pdf_x_and_y(pvals_m_mod)

        for cpg_id in tqdm(range(0, len(data_dicts[dataset]['item'])), desc=f'{dataset} processing'):

            pval_f = pvals_f[cpg_id]
            type_f = types_f[cpg_id]
            pval_m = pvals_m[cpg_id]
            type_m = types_m[cpg_id]

            if pval_f < pval_f_percentile and pval_m > pval_null_lim:
                for key in data_dicts[dataset]:
                    f_data_dicts[dataset][key].append(data_dicts[dataset][key][cpg_id])

            if pval_m < pval_m_percentile and pval_f > pval_null_lim:
                for key in data_dicts[dataset]:
                    m_data_dicts[dataset][key].append(data_dicts[dataset][key][cpg_id])

            if pval_f < pval_f_percentile and pval_m < pval_m_percentile and type_f != type_m:
                for key in data_dicts[dataset]:
                    fm_data_dicts[dataset][key].append(data_dicts[dataset][key][cpg_id])

    f_plot_data = []
    m_plot_data = []

    f_max = 1.15 * max([max(f_ys[dataset]) for dataset in data_dicts])
    m_max = 1.15 * max([max(m_ys[dataset]) for dataset in data_dicts])

    for d_id, dataset in enumerate(data_dicts):

        color = cl.scales['8']['qual']['Set1'][d_id]
        coordinates = color[4:-1].split(',')
        color_border = 'rgba(' + ','.join(coordinates) + ',' + str(0.8) + ')'

        scatter = go.Scatter(
            x=f_xs[dataset],
            y=f_ys[dataset],
            name=dataset,
            mode='lines',
            line=dict(
                width=4,
                color=color_border
            ),
            showlegend=True
        )
        f_plot_data.append(scatter)

        scatter = go.Scatter(
            x=[-np.log10(f_percentiles[dataset])]*2,
            y=[0, f_max],
            mode='lines',
            line=dict(
                width=4,
                color=color_border,
                dash='dot'
            ),
            showlegend=False
        )
        f_plot_data.append(scatter)

        scatter = go.Scatter(
            x=m_xs[dataset],
            y=m_ys[dataset],
            name=dataset,
            mode='lines',
            line=dict(
                width=4,
                color=color_border
            ),
            showlegend=True
        )
        m_plot_data.append(scatter)

        scatter = go.Scatter(
            x=[-np.log10(m_percentiles[dataset])]*2,
            y=[0, m_max],
            mode='lines',
            line=dict(
                width=4,
                color=color_border,
                dash='dot'
            ),
            showlegend=False
        )
        m_plot_data.append(scatter)

    layout = get_layout('$-log_{10}(pvalue)$', 'Probability density function')

    fn = f'{save_path}/f'
    figure = go.Figure(data=f_plot_data, layout=layout)
    figure.update_xaxes(range=[min([f_xs[dataset][0] for dataset in f_xs]), 1.3 * max([-np.log10(f_percentiles[dataset]) for dataset in f_percentiles])])
    figure.update_yaxes(range=[0, f_max])
    plotly.offline.plot(figure, filename=f'{fn}.html', auto_open=False, show_link=True)
    plotly.io.write_image(figure, f'{fn}.png')
    plotly.io.write_image(figure, f'{fn}.pdf')

    fn = f'{save_path}/m'
    figure = go.Figure(data=m_plot_data, layout=layout)
    figure.update_xaxes(range=[min([m_xs[dataset][0] for dataset in m_xs]), 1.3 * max([-np.log10(m_percentiles[dataset]) for dataset in m_percentiles])])
    figure.update_yaxes(range=[0, m_max])
    plotly.offline.plot(figure, filename=f'{fn}.html', auto_open=False, show_link=True)
    plotly.io.write_image(figure, f'{fn}.png')
    plotly.io.write_image(figure, f'{fn}.pdf')

    return f_data_dicts, m_data_dicts, fm_data_dicts


