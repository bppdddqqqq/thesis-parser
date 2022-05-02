"""A world eater of data into graphs"""
import os
from .plugins.truefalsegraph import export_binary_graph
import plotly.graph_objects as go
from ..categories import Category

def export_all():
    if not os.path.exists('dist'):
        os.mkdir('dist')
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
    for k, v in bool_graph_data.items():
        fig = go.Figure(data=[go.Pie(labels=['True', 'False', 'Unknown'], values=v['_v'], title=v['_n'], textinfo='value')])
        print(f"Printing bool figure... {k}")
        fig.write_image(f"dist/{k}.png")
        finished_figures.append(f"![[{k}.png]]")
    for k, v in string_graph_data.items():
        fig = go.Figure(data=[go.Pie(labels=list(v.keys()), values=list(v.values()), title=v['_n'])])
        print(f"Printing string figure... {k}")
        fig.write_image(f"dist/{k}.png")
        finished_figures.append(f"![[{k}.png]]")
    print("Done!")
    with open('dist/graphs.md', 'w') as fp:
        fp.write('\n'.join(finished_figures))
