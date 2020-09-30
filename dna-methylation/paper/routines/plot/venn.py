import plotly.graph_objs as go
import colorlover as cl

def get_trace_2(labels):
    trace = go.Scatter(
        x=[0.50, 2.50, 1.5],
        y=[1, 1, 1],
        text=labels,
        mode='text',
        textfont=dict(
            color='black',
            size=33,
            family='Arail',
        )
    )
    return trace

def get_trace_3(labels):
    trace = go.Scatter(
        x=[0.50, 1.5, 2.50, 0.87, 1.50, 2.10, 1.5],
        y=[0.75, 2.5, 0.75, 1.67, 0.67, 1.67, 1.4],
        text=labels,
        mode='text',
        textfont=dict(
            color='black',
            size=33,
            family='Arail',
        )
    )
    return trace

def get_trace_4(labels):
    trace = go.Scatter(
        x=[0.6, 0.7, 1.6, 2.85, 0.8, 1.9, 2.7, 1.45, 2.9, 2.15, 1.55, 2.73, 2.27, 2.2, 2.2],
        y=[-0.1, 1.1, 2.0, 1.8, 0.6, -0.2, 0.0, 1.25, 0.9, 1.9, 0.55, 0.45, 0.02, 1.2, 0.5],
        text=labels,
        mode='text',
        textfont=dict(
            color='black',
            size=33,
            family='Arail',
        )
    )
    return trace


def get_layout_2():
    colors = cl.scales['8']['qual']['Dark2'][0:4]
    layout = {
        'xaxis': {
            'showticklabels': False,
            'showgrid': False,
            'zeroline': False,
            'range': [0, 3]
        },
        'yaxis': {
            'showticklabels': False,
            'showgrid': False,
            'zeroline': False,
            'range': [0, 2]
        },
        'shapes': [
            {
                'opacity': 0.5,
                'xref': 'x',
                'yref': 'y',
                'fillcolor': colors[3],
                'x0': 0,
                'y0': 0,
                'x1': 2,
                'y1': 2,
                'type': 'circle',
                'line': {
                    'color': 'black'
                },
            },
            {
                'opacity': 0.5,
                'xref': 'x',
                'yref': 'y',
                'fillcolor': colors[2],
                'x0': 1,
                'y0': 0,
                'x1': 3,
                'y1': 2,
                'type': 'circle',
                'line': {
                    'color': 'black',
                },
            },
        ],
        'margin': {
            'l': 10,
            'r': 10,
            'b': 10,
            't': 10,
        },
        'height': 600,
        'width': 900,
        'plot_bgcolor': 'rgba(233,233,233,0)'
    }
    return layout

def get_layout_3():
    colors = cl.scales['8']['qual']['Dark2'][0:4]
    layout = {
        'xaxis': {
            'showticklabels': False,
            'showgrid': False,
            'zeroline': False,
            'range': [0, 3]
        },
        'yaxis': {
            'showticklabels': False,
            'showgrid': False,
            'zeroline': False,
            'range': [0, 3]
        },
        'shapes': [
            {
                'opacity': 0.5,
                'xref': 'x',
                'yref': 'y',
                'fillcolor': colors[3],
                'x0': 0,
                'y0': 0,
                'x1': 2,
                'y1': 2,
                'type': 'circle',
                'line': {
                    'color': 'black'
                },
            },
            {
                'opacity': 0.5,
                'xref': 'x',
                'yref': 'y',
                'fillcolor': colors[2],
                'x0': 1,
                'y0': 0,
                'x1': 3,
                'y1': 2,
                'type': 'circle',
                'line': {
                    'color': 'black',
                },
            },
            {
                'opacity': 0.5,
                'xref': 'x',
                'yref': 'y',
                'fillcolor': colors[1],
                'x0': 0.5,
                'y0': 1,
                'x1': 2.5,
                'y1': 3,
                'type': 'circle',
                'line': {
                    'color': 'black'
                },
            },
        ],
        'margin': {
            'l': 10,
            'r': 10,
            'b': 10,
            't': 10,
        },
        'height': 800,
        'width': 800,
        'plot_bgcolor': 'rgba(233,233,233,0)'
    }
    return layout

def get_layout_4():
    colors = cl.scales['8']['qual']['Dark2'][0:4]
    layout = {
        'xaxis': {
            'showticklabels': False,
            'showgrid': False,
            'zeroline': False,
            'range': [-0.05, 3.3]
        },
        'yaxis': {
            'showticklabels': False,
            'showgrid': False,
            'zeroline': False,
            'range': [-0.55, 3.05]
        },
        'shapes': [
            {
                'opacity': 0.5,
                'xref': 'x',
                'yref': 'y',
                'fillcolor': colors[0],
                'x0': 0,
                'y0': -0.5,
                'x1': 3,
                'y1': 1.0,
                'type': 'circle',
                'line': {
                    'color': 'black'
                },
            },
            {
                'opacity': 0.5,
                'xref': 'x',
                'yref': 'y',
                'fillcolor': colors[1],
                'x0': 0.2,
                'y0': 0.1,
                'x1': 3.2,
                'y1': 1.6,
                'type': 'circle',
                'line': {
                    'color': 'black',
                },
            },
            {
                'opacity': 0.5,
                'xref': 'x',
                'yref': 'y',
                'fillcolor': colors[3],
                'x0': 1.15,
                'y0': -0.45,
                'x1': 2.65,
                'y1': 2.55,
                'type': 'circle',
                'line': {
                    'color': 'black'
                },
            },
            {
                'opacity': 0.5,
                'xref': 'x',
                'yref': 'y',
                'fillcolor': colors[2],
                'x0': 1.75,
                'y0': -0.25,
                'x1': 3.25,
                'y1': 2.75,
                'type': 'circle',
                'line': {
                    'color': 'black'
                },
            },
        ],
        'margin': {
            'l': 10,
            'r': 10,
            'b': 10,
            't': 10,
        },
        'height': 1000,
        'width': 1000,
        'plot_bgcolor': 'rgba(233,233,233,0)'
    }

    return layout






