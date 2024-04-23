"""
Created on Tue Apr 21 13:58:52 2024

@author: oz_ge
"""


import pandas as pd
import altair as alt

with open("Problem.pickle", "rb") as f:
    Problem = pd.read_pickle(f)
    

optimized1=Problem.all_assignments[6].copy()
optimized2=Problem.all_assignments[7].copy()
optimized1 = optimized1.rename(columns={'Number of Students assigned': 'Number of Students'})

optimized = pd.concat([optimized1, optimized2], ignore_index=True)
optimized = optimized.drop('Utilization', axis=1)

# Merge the two DataFrames on a common column (Locations in this case)
optimized = pd.merge(optimized, Problem.Instance.room_data, left_on='Location', right_on='Locations', how='left')

# Drop the unnecessary 'Locations' column
optimized = optimized.drop(columns=['Locations'])
optimized = optimized[optimized['Term_Group'] == 'Group1']
#filter_building = optimized[optimized['Building'].isin(['Salisbury Labs','Stratton Hall', 'Olin Hall', 'Goddard Hall', 'Higgins Lab'])]

def Total_Dur_Week(formatted_pattern):
    days, start_time, end_time = formatted_pattern.split('_')
    # Extract start and end times as integers
    start_hr = int(start_time[:2])
    start_min = int(start_time[-2:])
    end_hr = int(end_time[:2])
    end_min = int(end_time[-2:])
    dur = len(days)*((end_hr - start_hr) + (end_min -start_min)/60)
    return round(dur,2)        
       
optimized['Total Duration'] = optimized['Pattern'].apply(Total_Dur_Week)
optimized['Utilization'] = optimized['Number of Students'] / optimized['Capacity']
#filter_building['Utilization'] = filter_building['Utilization'].apply(lambda x: f'{x:.0%}')
# Function to categorize "Type" column
def categorize_space_type(type_value):
    if 'lab' in type_value.lower():
        return 'Laboratory'
    else:
        return 'Teaching Space'

# Create a new "Space type" column based on the "Type" column
optimized['Space type'] = optimized['Type'].apply(categorize_space_type)
result_optimized = optimized.groupby('Location').agg({'Space type': 'max','Capacity':'max','Total Duration': 'sum', 'Utilization': 'mean'}).reset_index()

######ACTUAL

actual = Problem.Instance.df_.copy()
actual = pd.merge(actual, Problem.Instance.room_data, left_on='Location(s)', right_on='Locations', how='left')
actual = actual[actual['Academic Period'].isin(['2022 Fall A Term','2022 Fall Semester' ])]
actual = pd.merge(actual, Problem.Instance.df_pattern, left_on='Course_Section', right_on='Course_Section', how='left')
actual['Total Duration'] = actual['Pattern'].apply(Total_Dur_Week)
actual['Utilization'] = actual['Enrollment Count'] / actual['Capacity']
actual = actual[actual['Capacity'].notna()]

actual['Space type'] = actual['Type'].apply(categorize_space_type)
result_actual = actual.groupby('Locations').agg({'Space type': 'max','Capacity':'max','Total Duration': 'sum', 'Utilization': 'mean'}).reset_index()

####PLOT

brush = alt.selection_interval()

# Scatter plot for Actual data
scatter_actual = alt.Chart(result_actual).mark_circle().encode(
    x=alt.X('Total Duration', title='Total Duration', scale=alt.Scale(domain=[0, 65])),
    y=alt.Y('Utilization:Q', title='Utilization (%)',  scale=alt.Scale(domain=[0, 1.3]), axis=alt.Axis(format='%')),
    color=alt.Color('Space type:N', scale=alt.Scale(domain=['Laboratory', 'Teaching Space'], range=['#018571', '#dfc27d']), legend=None),
    size=alt.Size('Capacity:Q', scale=alt.Scale(range=[50, 1000]), legend=None),
    tooltip=['Locations', 'Capacity', 'Space type', 'Total Duration', 'Utilization']
).add_params(
    brush
).properties(
    title="Actual"
)

# Scatter plot for Optimized data
scatter_optimized = alt.Chart(result_optimized).mark_circle().encode(
    x=alt.X('Total Duration', title='Total Duration', scale=alt.Scale(domain=[0, 65])),
    y=alt.Y('Utilization:Q', title='Utilization (%)', scale=alt.Scale(domain=[0, 1.3]), axis=alt.Axis(format='%')),
    color=alt.Color('Space type:N', scale=alt.Scale(domain=['Laboratory', 'Teaching Space'], range=['#018571', '#dfc27d']), legend=None),
    size=alt.Size('Capacity:Q', scale=alt.Scale(range=[50, 1000]), legend=None),
    tooltip=['Location', 'Capacity', 'Space type', 'Total Duration', 'Utilization']
).add_params(
    brush
).properties(
    title="Optimized"
)

# Bar chart for Actual data responding to selection
bars_actual = alt.Chart(result_actual).mark_bar().encode(
    x=alt.X('count()', title='Count of Spaces'),
    y=alt.Y('Space type:N', title='Space Type'),
    color=alt.Color('Space type:N')
).transform_filter(
    brush
)

# Bar chart for Optimized data responding to selection
bars_optimized = alt.Chart(result_optimized).mark_bar().encode(
    x=alt.X('count()', title='Count of Spaces'),
    y=alt.Y('Space type:N', title='Space Type'),
    color=alt.Color('Space type:N')
).transform_filter(
    brush
)

# Combine scatter and bar charts side by side for both Actual and Optimized
combined_actual = scatter_actual & bars_actual
combined_optimized = scatter_optimized & bars_optimized

# Configure font sizes globally
combined_chart = (combined_actual | combined_optimized).configure(
    axis=alt.AxisConfig(labelFontSize=14, titleFontSize=16),
    legend=alt.LegendConfig(titleFontSize=14, labelFontSize=12)
)

# Save or display the chart
combined_chart.save('utilization_scatter.html')
