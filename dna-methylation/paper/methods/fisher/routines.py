import numpy as np
from scipy import stats as stats
import plotly.graph_objs as go
import plotly
import plotly.io as pio


def perform_fisher(x, n, m, N):
    contingency_table = [[x, m - x], [n - x, N - n - m + x]]
    print(contingency_table)
    a = np.sum(contingency_table, axis=0)
    b = np.sum(contingency_table, axis=1)
    if np.sum(a) == np.sum(b):
        print('contingency_table is ok')
    oddsratio, pvalue = stats.fisher_exact(contingency_table)
    return oddsratio, pvalue

def odds_ratio_plot(x_data, y_data, fn):

    traces = []
    for id in range(0, len(y_data)):
        if y_data[id] < 1.0:
            trace = go.Bar(
                x=[x_data[id]],
                y=[1 - y_data[id]],
                base=[y_data[id]],
                marker=dict(
                    color='rgba(55, 128, 191, 0.7)',
                    line=dict(
                        color='rgba(55, 128, 191, 1.0)',
                        width=2,
                    )
                )
            )
        else:
            trace = go.Bar(
                x=[x_data[id]],
                y=[y_data[id] - 1.0],
                base=[1.0],
                marker=dict(
                    color='rgba(55, 128, 191, 0.7)',
                    line=dict(
                        color='rgba(55, 128, 191, 1.0)',
                        width=2,
                    )
                )
            )
        traces.append(trace)

    layout = go.Layout(
        plot_bgcolor='rgba(233,233,233,0)',
        barmode='overlay',
        showlegend=False,
        autosize=True,
        margin=go.layout.Margin(
            l=120,
            r=20,
            b=120,
            t=20,
            pad=0
        ),
        yaxis=dict(
            gridcolor='rgb(100, 100, 100)',
            gridwidth=0.01,
            mirror=True,
            linecolor='black',
            title='Odds ratio',
            type='log',
            autorange=True,
            showgrid=True,
            showline=True,
            titlefont=dict(
                family='Arial',
                size=25,
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
            #tickvals=[0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10],
        ),
        xaxis=dict(
            gridcolor='rgb(100, 100, 100)',
            mirror=True,
            linecolor='black',
            autorange=True,
            showgrid=False,
            showline=True,
            tickangle=90,
            titlefont=dict(
                family='Arial',
                size=20,
                color='black'
            ),
            showticklabels=True,
            tickfont=dict(
                family='Arial',
                size=20,
                color='black'
            ),
            exponentformat='e',
            showexponent='all',
        ),
    )

    fig = go.Figure(data=traces, layout=layout)

    plotly.offline.plot(fig, filename=fn + '.html', auto_open=False, show_link=True)
    pio.write_image(fig, fn + '.png')
    pio.write_image(fig, fn + '.pdf')