import plotly.graph_objects as go

def export_binary_graph(path='/null.png', values=[1,1,1], title='Default'):
    fig = go.Figure(data=[go.Pie(labels=['True', 'False', 'Unknown'], values=values, title=title, textinfo='value')])
    fig.write_image(path)

