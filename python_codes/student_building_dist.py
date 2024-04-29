# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 09:39:33 2024

@author: oz_ge
"""

import altair as alt
import pandas as pd

source = pd.read_excel("C:/Users/oz_ge/Timetabling/Extended Framework/Student_Distribution_by_Day_Time_Building.xlsx")

# Points for the interactive selection
pts = alt.selection_point(encodings=['x'])

rect = alt.Chart(source).mark_rect().encode(
    alt.X('Time Block:O').bin(),
    alt.Y('Day:O').bin(),
    alt.Color('sum(Number of Students):Q').scale(scheme='greenblue').title('Number of Students')
)

circ = rect.mark_point().encode(
    alt.ColorValue('grey'),
    alt.Size('sum(Number of Students):Q').title('Number of Students in Selection')
).transform_filter(
    pts
)

bar = alt.Chart(source, width=550, height=200).mark_bar().encode(
    x='Building:N',
    y='sum(Number of Students):Q',
    color=alt.condition(pts, alt.ColorValue("steelblue"), alt.ColorValue("grey"))
).add_params(pts)

alt.vconcat(
    rect + circ,
    bar
).resolve_legend(
    color="independent",
    size="independent"
)




# The heatmap chart
heatmap = alt.Chart(source).mark_rect().encode(
    alt.X('Time Block:N', title='Time Block'),
    alt.Y('Day:N', title='Day'),
    alt.Color('sum(Number of Students):Q', scale=alt.Scale(scheme='greenblue'), title='Number of Students')
)

circ = heatmap.mark_point().encode(
    alt.ColorValue('grey'),
    alt.Size('Number of Students:Q', title='Number of Students in Selection')
).transform_filter(
    pts
)

# The bar chart for buildings
bar = alt.Chart(source, width=550, height=200).mark_bar().encode(
    x='Building:N',
    y='sum(Number of Students):Q',
    color=alt.condition(pts, alt.ColorValue("steelblue"), alt.ColorValue("grey"))
).add_params(pts)

# Combine the charts vertically
chart = alt.vconcat(
    heatmap + circ,
    bar
).resolve_legend(
    color="independent",
    size="independent"
)
    
chart.save('building_student_dist.html')
