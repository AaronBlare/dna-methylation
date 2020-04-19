import plotly.graph_objs as go
import colorlover as cl
import numpy as np
from paper.routines.infrastructure.save.figure import save_figure

def minus_log_pvals_figure(pvals, pvals_percentiles, save_path, num_bins=1000):

    max_x = 20
    min_x = 0.0

    shift = (max_x - min_x) / num_bins
    x = [min_x + (shift / 2) + i * shift for i in range(0, num_bins)]

    for dataset in pvals:

        curr_plot_data = []
        lines = []
        max_y = -1
        min_y = 100000000

        for obs in pvals[dataset]:

            y = [0] * num_bins
            num_outliers = 0
            for curr_R2 in pvals[dataset][obs]:
                if curr_R2 > max_x or curr_R2 < min_x:
                    num_outliers += 1
                else:
                    index = int(np.floor((curr_R2 - min_x) / (max_x - min_x + 1e-10) * num_bins))
                    y[index] += 1

            sum_y = np.sum(y)
            y = [curr_y / (sum_y * shift) for curr_y in y]
            if min(y) < min_y:
                min_y = min(y)
            if max(y) > max_y:
                max_y = max(y)

            # Colors setup
            color = cl.scales['8']['qual']['Set1'][list(pvals[dataset].keys()).index(obs)]
            coordinates = color[4:-1].split(',')
            color_border = 'rgba(' + ','.join(coordinates) + ',' + str(0.8) + ')'

            scatter = go.Scatter(
                x=x,
                y=y,
                name=f'{dataset}_{obs}',
                mode='lines',
                line=dict(
                    width=4,
                    color=color_border
                ),
            )
            curr_plot_data.append(scatter)

            curr_line = {
                'type': 'line',
                'x0': pvals_percentiles[dataset][obs][0],
                'y0': min_y,
                'x1': pvals_percentiles[dataset][obs][0],
                'y1': max_y,
                'line': {
                    'color': color_border,
                    'width': 2,
                },
            }

            lines.append(curr_line)

        layout = go.Layout(
            autosize=True,
            barmode='overlay',
            legend=dict(
                font=dict(
                    family='Arial',
                    size=16,
                ),
                orientation="h",
                x=0.11,
                y=1.11,
            ),
            margin=go.layout.Margin(
                l=95,
                r=10,
                b=80,
                t=85,
                pad=0
            ),
            shapes=lines,
            xaxis=dict(
                exponentformat='e',
                mirror='ticks',
                showexponent='all',
                showgrid=True,
                showline=True,
                showticklabels=True,
                tickangle=0,
                tickfont=dict(
                    color='black',
                    family='Arial',
                    size=30
                ),
                title=dict(
                    font=dict(
                        color='black',
                        family='Arial',
                        size=50),
                    text=r'$R^2$')
            ),
            yaxis=dict(
                title='PDF',
                showgrid=True,
                showline=True,
                mirror='ticks',
                titlefont=dict(
                    family='Arial',
                    size=33,
                    color='black'
                ),
                showticklabels=True,
                tickangle=0,
                tickfont=dict(
                    family='Arial',
                    size=30,
                    color='black'
                ),
                exponentformat='e',
                showexponent='all'
            )
        )

        figure = go.Figure(data=curr_plot_data, layout=layout)
        save_figure(f'{save_path}/{dataset}_pvalues', figure)
