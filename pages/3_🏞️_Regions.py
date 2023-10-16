import streamlit as st
from utils import compute_pdk_column_map, list_elig, list_techno, elig_color, techno_color, region_list, department_list, color_to_hex, color_to_alt, compute_folium_map, load_data_departement
import altair as alt
from millify import millify
import plotly.express as px
from streamlit_folium import folium_static
from time import time

st.set_page_config(layout="wide", page_title='Ma Connexion Internet Analysis in France',
                   page_icon='📶', initial_sidebar_state='auto')

st.header('Visualization for one region', divider="rainbow")

start = time()
df = load_data_departement()
st.toast(f"Data loaded in {time() - start:.2f} seconds")

region_select = st.selectbox(
    'Select the region', sorted(df['Region Code'].unique()), index=0, key='region', format_func=lambda x: region_list[str(x)])

df = df[df['Region Code'] == region_select]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Number of entity", millify(df[df['Year'] == 2023]['Entity Number'].sum()), delta=millify(
        df[df['Year'] == 2023]['Entity Number'].sum() - df[df['Year'] == 2022]['Entity Number'].sum()))
    st.metric("Number of department", df['Department Code'].nunique())

with col2:
    st.metric("Entity fiber eligible", millify(df[df['Year'] == 2023]['Fiber'].sum()), delta=millify(
        df[df['Year'] == 2023]['Fiber'].sum() - df[df['Year'] == 2022]['Fiber'].sum()))
    st.metric("Entity cellular eligible", millify(df[df['Year'] == 2023]['Cellular'].sum()), delta=millify(
        df[df['Year'] == 2023]['Cellular'].sum() - df[df['Year'] == 2022]['Cellular'].sum()))

with col3:
    st.metric("Number of ineligible entity ", millify(df[df['Year'] == 2023]['Ineligible entity'].sum()), delta=millify(
        df[df['Year'] == 2023]['Ineligible entity'].sum() - df[df['Year'] == 2022]['Ineligible entity'].sum()), delta_color='inverse')
    st.metric("Entity eligible - > 30 Mbit/s", millify(df[df['Year'] == 2023][['> 30 Mbit/s', '> 100 Mbit/s', '> 1 Gbit/s']].sum().sum()), delta=millify(
        df[df['Year'] == 2023][['> 30 Mbit/s', '> 100 Mbit/s', '> 1 Gbit/s']].sum().sum() - df[df['Year'] == 2022][['> 30 Mbit/s', '> 100 Mbit/s', '> 1 Gbit/s']].sum().sum()))


"""
---
Coorelation between the different columns
"""
toggle_coor = st.toggle('Show the correlation matrix by year', value=False)
df_toggle = df

if toggle_coor:
    year_coor = st.slider('Select the year', min_value=2020,
                          max_value=2023, value=2023, step=1, key='coor')

    df_toggle = df[df['Year'] == year_coor]


st.plotly_chart(px.imshow(df_toggle.drop(['Department Name', 'Department Code', 'Region Code', 'geometry', 'Entity Number'], axis=1).corr(
), zmin=-1, zmax=1, width=800, height=800, color_continuous_scale='BuPu'))

"""
---
Evolution of the internet speed eligibylity by year
"""

st.altair_chart(alt.Chart(df.drop(['geometry', 'Region Code'], axis=1).groupby(['Year']).sum().reset_index().melt(id_vars=['Year'], value_vars=list_elig, var_name='Eligibility', value_name='Sum')).mark_line().encode(
    x='Year:O',
    y=alt.Y('Sum', scale=alt.Scale(type='log', clamp=True, domainMin=1)),
    color=alt.Color('Eligibility', scale=color_to_alt(elig_color)),
).interactive(), use_container_width=True)

"""
---
Pie chart of the number of the internet speed eligibility by year
"""

year_pie = st.slider('Select the year', min_value=2020,
                     max_value=2023, value=2023, step=1, key='elig')

st.plotly_chart(px.pie(df[df['Year'] == year_pie].drop(['geometry', 'Region Code'], axis=1).groupby(['Year']).sum().reset_index().melt(id_vars=['Year'], value_vars=list_elig, var_name='Eligibility', value_name='Sum'),
                       values='Sum', names='Eligibility', color='Eligibility', color_discrete_map=color_to_hex(elig_color)))

"""
---
Map of the region by cumulative internet speed eligibility ratio
"""

option_elig = st.selectbox('Select the eligibility',
                           list_elig, index=0, key='map_elig')

option_year = st.slider('Select the year', min_value=2020,
                        max_value=2023, value=2023, step=1, key='map_elig_year')

df_map = df[df['Year'] == option_year].copy()
df_map[list_elig[:0:-1]] = df_map[list_elig[:0:-1]].cumsum(axis=1)
df_map = df_map.assign(ratio=df_map[option_elig] / df_map['Entity Number'])

m = compute_folium_map(df_map, 'Region Code', 'ratio',
                       f'Ratio of eligible entity to {option_elig}', bins=[0, 0.25, 0.5, 0.75, 1])

folium_static(m)

"""
---
Evolution of the technology eligibility by year
"""

st.altair_chart(alt.Chart(df.drop(['geometry', 'Region Code', 'Department Name'], axis=1).groupby(['Year']).sum().reset_index().melt(id_vars=['Year'], value_vars=list_techno, var_name='Technology', value_name='Sum')).mark_line().encode(
    x='Year:O',
    y=alt.Y('Sum', scale=alt.Scale(
        type='log', clamp=True, domainMin=1)),
    color=alt.Color('Technology', scale=color_to_alt(techno_color)),
).interactive(), use_container_width=True)

"""
---
Pie chart of the number of entity by technology by year
"""

year_pie = st.slider('Select the year', min_value=2020,
                     max_value=2023, value=2023, step=1, key='techno')

st.plotly_chart(px.pie(df[df['Year'] == year_pie].drop(['geometry'], axis=1).groupby(['Year']).sum().reset_index().melt(id_vars=['Year'], value_vars=list_techno, var_name='Technology', value_name='Sum'),
                       values='Sum', names='Technology', color='Technology', color_discrete_map=color_to_hex(techno_color)))


"""
---
Map of the technology eligibility
"""

option_year = st.slider('Select the year', min_value=2020,
                        max_value=2023, value=2023, step=1, key='map_tech_col_year')

df_map = df[df['Year'] == option_year].copy()
df_map['lon'] = df_map['geometry'].centroid.x
df_map['lat'] = df_map['geometry'].centroid.y


m, legend = compute_pdk_column_map(
    df_map, list_techno, radius=2000, elevation_scale=0.01, color=techno_color, zoom=7,
    tooltip={'text': "Department: {Department Name} ({Department Code})\n Eligible entity: {Entity Number} \n" + '\n'.join([f"{tech}: {{{tech}}}" for tech in list_techno])})

st.pydeck_chart(m)

"Legend:"

st.write(legend, unsafe_allow_html=True)

"""
---
Barplot of the number of ineligible entity by department by year
"""

df_bar = df.drop(['geometry'], axis=1).groupby(
    ['Year', 'Department Code']).sum().reset_index()[['Year', 'Department Code', 'Ineligible entity']]

df_bar['Department Code'] = df_bar['Department Code'].apply(
    lambda x: department_list[str(x)])

st.bar_chart(df_bar.pivot(index='Department Code',
             columns='Year', values='Ineligible entity'))
