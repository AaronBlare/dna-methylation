import copy
from collections import defaultdict
from tqdm import tqdm
from paper.routines.plot.pdf import get_pdf_x_and_y
from paper.routines.plot.layout import get_layout
import plotly.graph_objs as go
import colorlover as cl
import plotly
import numpy as np


def add_best_pvalue(data_dicts, p_value_prefix):

    for dataset in data_dicts:

        lin_lin_pvals = data_dicts[dataset][f'lin_lin_{p_value_prefix}']
        lin_log_pvals = data_dicts[dataset][f'lin_log_{p_value_prefix}']
        log_lin_pvals = data_dicts[dataset][f'log_lin_{p_value_prefix}']
        log_log_pvals = data_dicts[dataset][f'log_log_{p_value_prefix}']

        # data_dicts[dataset][p_value_prefix] = np.minimum(np.minimum(lin_lin_pvals, lin_log_pvals), np.minimum(log_lin_pvals, log_log_pvals))
        data_dicts[dataset][p_value_prefix] = lin_lin_pvals

def filter_data_dicts(data_dicts, p_value_prefix, pval_perc_ss, pval_perc_ar, pval_lim, save_path):

    ss_data_dicts = dict.fromkeys(data_dicts.keys())
    for dd in ss_data_dicts:
        ss_data_dicts[dd] = defaultdict(list)
    ar_data_dicts = copy.deepcopy(ss_data_dicts)
    ssar_data_dicts = copy.deepcopy(ss_data_dicts)

    ss_xs = dict.fromkeys(data_dicts.keys())
    ss_ys = dict.fromkeys(data_dicts.keys())

    ar_xs = dict.fromkeys(data_dicts.keys())
    ar_ys = dict.fromkeys(data_dicts.keys())

    ss_percentiles = {}
    ar_percentiles = {}

    for dataset in data_dicts:

        pvals_ss = np.array(data_dicts[dataset][f'{p_value_prefix}_ss'])
        pvals_ar = np.array(data_dicts[dataset][f'{p_value_prefix}_ar'])
        # pval_ss_percentile = min(np.percentile(pvals_ss, pval_perc_ss), pval_lim)
        # pval_ar_percentile = min(np.percentile(pvals_ar, pval_perc_ar), pval_lim)
        pval_ss_percentile = 0.01
        pval_ar_percentile = 0.01
        print(f'{dataset} ss percentile: {pval_ss_percentile}')
        print(f'{dataset} ar percentile: {pval_ar_percentile}')
        ss_percentiles[dataset] = pval_ss_percentile
        ar_percentiles[dataset] = pval_ar_percentile

        pvals_ss_mod = -np.log10(pvals_ss[np.nonzero(pvals_ss)])
        ss_xs[dataset], ss_ys[dataset] = get_pdf_x_and_y(pvals_ss_mod)
        pvals_ar_mod = -np.log10(pvals_ar[np.nonzero(pvals_ar)])
        ar_xs[dataset], ar_ys[dataset] = get_pdf_x_and_y(pvals_ar_mod)

        for cpg_id in tqdm(range(0, len(data_dicts[dataset]['item'])), desc=f'{dataset} processing'):

            pval_ss = pvals_ss[cpg_id]
            pval_ar = pvals_ar[cpg_id]

            if pval_ss < pval_ss_percentile:
                for key in data_dicts[dataset]:
                    ss_data_dicts[dataset][key].append(data_dicts[dataset][key][cpg_id])

            if pval_ar < pval_ar_percentile:
                for key in data_dicts[dataset]:
                    ar_data_dicts[dataset][key].append(data_dicts[dataset][key][cpg_id])

            if pval_ss < pval_ss_percentile and pval_ar < pval_ar_percentile:
                for key in data_dicts[dataset]:
                    ssar_data_dicts[dataset][key].append(data_dicts[dataset][key][cpg_id])

    ss_plot_data = []
    ar_plot_data = []

    ss_max = 1.15 * max([max(ss_ys[dataset]) for dataset in data_dicts])
    ar_max = 1.15 * max([max(ar_ys[dataset]) for dataset in data_dicts])

    for d_id, dataset in enumerate(data_dicts):

        color = cl.scales['8']['qual']['Set1'][d_id]
        coordinates = color[4:-1].split(',')
        color_border = 'rgba(' + ','.join(coordinates) + ',' + str(0.8) + ')'

        scatter = go.Scatter(
            x=ss_xs[dataset],
            y=ss_ys[dataset],
            name=dataset,
            mode='lines',
            line=dict(
                width=4,
                color=color_border
            ),
            showlegend=True
        )
        ss_plot_data.append(scatter)

        scatter = go.Scatter(
            x=[-np.log10(ss_percentiles[dataset])]*2,
            y=[0, ss_max],
            mode='lines',
            line=dict(
                width=4,
                color=color_border,
                dash='dot'
            ),
            showlegend=False
        )
        ss_plot_data.append(scatter)

        scatter = go.Scatter(
            x=ar_xs[dataset],
            y=ar_ys[dataset],
            name=dataset,
            mode='lines',
            line=dict(
                width=4,
                color=color_border
            ),
            showlegend=True
        )
        ar_plot_data.append(scatter)

        scatter = go.Scatter(
            x=[-np.log10(ar_percentiles[dataset])]*2,
            y=[0, ar_max],
            mode='lines',
            line=dict(
                width=4,
                color=color_border,
                dash='dot'
            ),
            showlegend=False
        )
        ar_plot_data.append(scatter)

    layout = get_layout('$-log_{10}(pvalue)$', 'Probability density function')

    fn = f'{save_path}/ss'
    figure = go.Figure(data=ss_plot_data, layout=layout)
    figure.update_xaxes(range=[min([ss_xs[dataset][0] for dataset in ss_xs]), 1.3 * max([-np.log10(ss_percentiles[dataset]) for dataset in ss_percentiles])])
    figure.update_yaxes(range=[0, ss_max])
    plotly.offline.plot(figure, filename=f'{fn}.html', auto_open=False, show_link=True)
    plotly.io.write_image(figure, f'{fn}.png')
    plotly.io.write_image(figure, f'{fn}.pdf')

    fn = f'{save_path}/ar'
    figure = go.Figure(data=ar_plot_data, layout=layout)
    figure.update_xaxes(range=[min([ar_xs[dataset][0] for dataset in ar_xs]), 1.3 * max([-np.log10(ar_percentiles[dataset]) for dataset in ar_percentiles])])
    figure.update_yaxes(range=[0, ar_max])
    plotly.offline.plot(figure, filename=f'{fn}.html', auto_open=False, show_link=True)
    plotly.io.write_image(figure, f'{fn}.png')
    plotly.io.write_image(figure, f'{fn}.pdf')

    return ss_data_dicts, ar_data_dicts, ssar_data_dicts


