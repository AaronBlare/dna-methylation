import plotly.graph_objs as go


def get_layout(x_name, y_name):

    layout = go.Layout(
        plot_bgcolor='rgba(233,233,233,0)',
        autosize=True,
        barmode='overlay',
        legend=dict(
            font=dict(
                family='Arial',
                size=16,
            ),
            orientation="h",
            x=0.1,
            y=1.1,
        ),
        margin=go.layout.Margin(
            l=80,
            r=20,
            b=80,
            t=10,
            pad=0
        ),
        xaxis=dict(
            exponentformat='e',
            showexponent='all',
            showgrid=False,
            linewidth=2,
            linecolor='black',
            showline=True,
            gridcolor='rgb(100, 100, 100)',
            gridwidth=0.01,
            mirror=True,
            showticklabels=True,
            tickangle=0,
            tickfont=dict(
                color='black',
                family='Arial',
                size=16
            ),
            title=dict(
                font=dict(
                    color='black',
                    family='Arial',
                    size=20),
                text=x_name)
        ),
        yaxis=dict(
            exponentformat='e',
            showexponent='all',
            showgrid=False,
            linewidth=2,
            linecolor='black',
            showline=True,
            gridcolor='rgb(100, 100, 100)',
            gridwidth=0.01,
            mirror=True,
            showticklabels=True,
            tickangle=0,
            tickfont=dict(
                family='Arial',
                size=16,
                color='black'
            ),
            title = dict(
                    font=dict(
                        color='black',
                        family='Arial',
                        size=20),
                    text=y_name)
        )
    )

    return layout