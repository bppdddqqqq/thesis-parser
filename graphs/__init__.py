"""A world eater of data into graphs"""
import os
from .plugins.truefalsegraph import export_binary_graph
import plotly.graph_objects as go
from ..categories import Category
import plotly.express as px
from ..tables import fetch_table, fetch_cats
MAIN_LOC = 'dist/graphs/'

def transform_to_percentages(array):
    s = sum(array)
    return list(map(lambda x: round(((x*1.0)/s)*100, 1), array))

def summarised_graph_bool(bool_graph_data):
    top_labels = ['True', 'False']
    
    graph = sorted(bool_graph_data.items())
    x_data = map(lambda x: transform_to_percentages(x[1]['_v'][0:2]), graph)
    y_data = map(lambda x: x[1]['_n'], graph)
    x_data = list(x_data)
    y_data = list(y_data)

    colors = ['rgba(38, 24, 74, 0.8)', 'rgba(71, 58, 131, 0.8)',
          'rgba(122, 120, 168, 0.8)', 'rgba(164, 163, 204, 0.85)',
          'rgba(190, 192, 213, 1)']

    fig = go.Figure()

    for i in range(0, len(top_labels)):
        for xd, yd in zip(x_data, y_data):
            fig.add_trace(go.Bar(
                x=[xd[i]], y=[yd],
                orientation='h',
                marker=dict(
                    color=colors[i],
                    line=dict(color='rgb(248, 248, 249)', width=1)
                )
            ))

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0.15, 1]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        barmode='stack',
        paper_bgcolor='rgb(248, 248, 255)',
        plot_bgcolor='rgb(248, 248, 255)',
        margin=dict(l=120, r=10, t=140, b=80),
        showlegend=False,
    )

    annotations = []

    for yd, xd in zip(y_data, x_data):
        # labeling the y-axis
        annotations.append(dict(xref='paper', yref='y',
                                x=0.14, y=yd,
                                xanchor='right',
                                text=str(yd),
                                font=dict(family='Arial', size=14,
                                          color='rgb(67, 67, 67)'),
                                showarrow=False, align='right'))
        # labeling the first percentage of each bar (x_axis)
        annotations.append(dict(xref='x', yref='y',
                                x=xd[0] / 2, y=yd,
                                text=str(xd[0]) + '%',
                                font=dict(family='Arial', size=14,
                                          color='rgb(248, 248, 255)'),
                                showarrow=False))
        # labeling the first Likert scale (on the top)
        if yd == y_data[-1]:
            annotations.append(dict(xref='x', yref='paper',
                                    x=xd[0] / 2, y=1.1,
                                    text=top_labels[0],
                                    font=dict(family='Arial', size=14,
                                              color='rgb(67, 67, 67)'),
                                    showarrow=False))
        space = xd[0]
        for i in range(1, len(xd)):
            # labeling the rest of percentages for each bar (x_axis)
            annotations.append(dict(xref='x', yref='y',
                                    x=space + (xd[i]/2), y=yd,
                                    text=str(xd[i]) + '%',
                                    font=dict(family='Arial', size=14,
                                              color='rgb(248, 248, 255)'),
                                    showarrow=False))
            # labeling the Likert scale
            if yd == y_data[-1]:
                annotations.append(dict(xref='x', yref='paper',
                                        x=space + (xd[i]/2), y=1.1,
                                        text=top_labels[i],
                                        font=dict(family='Arial', size=14,
                                                  color='rgb(67, 67, 67)'),
                                        showarrow=False))
            space += xd[i]

    fig.update_layout(annotations=annotations)

    path = f"{MAIN_LOC}/summarised_bool.png"
    fig.write_image(path)
    return path

def export_all():
    os.makedirs(MAIN_LOC, exist_ok=True)
    bool_graph_data = {}
    string_graph_data = {}
    for k, v in Category.known.items():
        if len(v.associated_value) == 0:
            continue
        # if bool, use ternary validator
        if v.primitive_type == 'Bool':
            bool_graph_data[k] = { '_n': v.title, '_v': [0,0,0] }
            for values in v.associated_value:
                res = values.value
                if res is None:
                    bool_graph_data[k]['_v'][2] += 1
                else:
                    bool_graph_data[k]['_v'][0 if res else 1] += 1
        if v.primitive_type == 'String' or v.primitive_type == 'StringNone': 
            string_graph_data[k] = { '_n': v.title }
            for values in v.associated_value:
                res = values.value
                if res is None:
                    string_graph_data[k]['Unknown'] = string_graph_data[k].get('Unknown', 0) + 1
                else:
                    string_graph_data[k][res] = string_graph_data[k].get(res, 0) + 1
    finished_figures = []
    print("Printing figures...")
    print("Printing all bool figure...")
    finished_figures.append(summarised_graph_bool(bool_graph_data))
    for k, v in bool_graph_data.items():
        fig = go.Figure(data=[go.Pie(labels=['True', 'False', 'Unknown'], values=v['_v'], title=v['_n'], textinfo='value')])
        print(f"Printing bool figure... {k}")
        fig.write_image(f"{MAIN_LOC}/{k}.png")
        finished_figures.append(f"![[{k}.png]]")
    for k, v in string_graph_data.items():
        fig = go.Figure(data=[go.Pie(labels=list(v.keys()), values=list(v.values()), title=v['_n'])])
        print(f"Printing string figure... {k}")
        fig.write_image(f"{MAIN_LOC}/{k}.png")
        finished_figures.append(f"![[{k}.png]]")
    
    print("Done!")
    with open('dist/graphs.md', 'w') as fp:
        fp.write('\n'.join(finished_figures))
