import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import missingno as msno
import folium as fo
import geopandas as gpd
import altair as alt
import pydeck as pdk
from utils import columns_description, load_data_region, techno_description


st.set_page_config(layout="wide", page_title='Ma Connexion Internet Analysis in France',
                   page_icon='📶', initial_sidebar_state='auto')

df = load_data_region()

st.header('Introduction', divider="rainbow")

st.snow()

"""
In this analysis, we are looking into a dataset of the internet connection speed in France by commune and region. 
The dataset is available on the [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/ma-connexion-internet/) website.
The dataset is updated every trimester without any missing value and for this visualisation, we are looking at the data from 2020 to 2023.

The dataset contains the following information:
"""

st.table(pd.DataFrame.from_dict(columns_description,
         orient='index', columns=['Description']))

"""
Before going further, you have to know some fact about the internet technology used in France and the debit associated with it.
"""
st.table(techno_description)

"""
Here is what the dataset looks like:
"""

st.dataframe(df.drop('geometry', axis=1))

"""
You also can look at the data documentation [here](https://www.data.gouv.fr/fr/datasets/r/8c21e6a5-ebcb-4eaf-b835-a687abce248d).
"""
