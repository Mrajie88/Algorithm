import plotly.plotly as py
from plotly import tools
from plotly.graph_objs import *
tools.set_credentials_file(username='Worldzhang', api_key='OU3H87MJxDBEGP45zQa3')

trace0 = Scatter(
    x=[1, 2, 3],
    y=[10, 15, 13],
    marker=dict(
        color=['red','blue','green'],
        size=[30,80,200],
    ),
     mode='markers'
)

data = Data([trace0])

py.iplot(data)
