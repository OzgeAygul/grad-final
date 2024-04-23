# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 15:27:43 2024

@author: oz_ge
"""

import plotly.graph_objects as go

# Data
num_add_stu = [-150, -100, -50, 0, 50, 100, 150]
sp_ovs_b = [14, 15, 16, 18, 25, 28, 42]
sp_ovs_s = [3, 4, 3, 3, 4, 4, 4]
spl_sp = [8, 11, 16, 19, 27, 31, 44]

# Create traces
trace1 = go.Scatter(x=num_add_stu, y=sp_ovs_b, mode='lines', name='Bottleneck Sections (Before Splitting)', line=dict(color='#2b83ba', width=3))
trace2 = go.Scatter(x=num_add_stu, y=sp_ovs_s, mode='lines', name='Bottleneck Sections (After Splitting)', line=dict(color='#fdae61', width=3))
trace3 = go.Scatter(x=num_add_stu, y=spl_sp, line_shape='hv', mode='lines+markers', name='Splits', line=dict(color='#d7191c', width=3, dash='dash'), yaxis='y2')

layout = go.Layout(
    title='Impact of Enrollment Changes on Course Scheduling',
    xaxis=dict(title='Scaled Enrollment'),
    yaxis=dict(title='Number of Bottleneck Sections', side='left'),
    yaxis2=dict(title='Number of Splits', side='right', overlaying='y'),
    legend=dict(x=0.3, y=1.15, orientation='h'),
    margin=dict(l=40, r=40, t=40, b=30),
    plot_bgcolor='white'
)

fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)
fig.write_html('tradeoff.html')  # Save the plot as an HTML file
