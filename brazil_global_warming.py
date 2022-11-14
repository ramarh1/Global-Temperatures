import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle
import plotly.graph_objs as go

st.set_page_config(
    page_title="Environment Dashboard",
    page_icon="random",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title('Global Warming Trends in Different Countries')
data = pd.read_csv("archive/ENVIRON_DATA.csv")
ghg_df = pd.read_csv("archive/greenhouse.csv")

def preprocess_data(df):
    df = df.copy()
    df = df.query("Element == 'Temperature change'")
    df_grouped = df.groupby("Area").mean()
    df_grouped.reset_index()
    df_grouped.drop(df_grouped.columns[[0,1,2,3,4]], inplace=True, axis=1)
    df_grouped.rename(columns=lambda x: x[1:], inplace=True)

    return df_grouped

updated_data = preprocess_data(data)
updated_data = updated_data.reset_index()

st.caption("Dataframe displaying temperature difference of different countries.")
st.dataframe(updated_data)
country_list = updated_data.Area.values.tolist()

def query_country(df, name):
    #df2 = df.query(f"Area == '{name}'")
    df = df.T
    df = df.rename_axis("Year")
    df = df.rename(columns= lambda x: "Temp Change")
    df = df.reset_index(drop=False)
    df = df[1:]
    
    dfs = {country: df[df["country"] == country] for country in country_stats}
    fig = go.Figure()
    for country, df in dfs.items():
        fig = fig.add_trace(go.Scatter(x=df["Year"], y=df["Temp Change"], name=country))
    st.plotly_chart(fig)


option = st.multiselect('Choose a country to see the global warming trend:',country_list)
result1 = st.button("Click button when finished with multiselect.",key=19)

if(result1 == True):
    st.header("You selected: {}".format(", ".join(option)))
    st.caption("Line chart displaying temperature difference of different countries from 1961-2019.")
    country_stats = query_country(updated_data,option)

#st.line_chart(country_stats,x="Year",y="Temp Change")

deforest_df = pd.read_csv("archive/annual-deforestation.csv")
deforest_df = deforest_df.drop(columns="Code")
deforest_df = deforest_df[4:]
deforest_df = deforest_df.query("Entity != 'South America' and Entity != 'World'")
deforest_list = deforest_df.Entity.values.tolist()

def query_country2(df,name):
    df = df.query(f"Entity == '{name}'")
    return df

file = "archive/earth.jpg"
st.image(file)

st.image("archive/unsplash.jpg")
deforest_list = [*set(deforest_list)]
deforest_list = sorted(deforest_list)
deforest_option = st.selectbox('Choose a country to see the deforestation trend:',deforest_list)
deforest_stats = query_country2(deforest_df,deforest_option)

st.caption("Bar chart displaying deforestation trends across the world at different time periods up until 2015.")
st.bar_chart(deforest_stats, x='Year',y='Deforestation')

# GHG Section of webpage
ghg_df = ghg_df.rename(columns={"country_or_area": "country"})
GHG_countries = ghg_df.country.unique().tolist()
ghg_df['year'] = ghg_df['year'].astype(str)
GHG_option = st.multiselect('Choose one or more countries to view the GHG emissions in million metric tons from 1990-2014',GHG_countries)

result = st.button("Click button when finished with multiselect.", key=20)
cycol = cycle('bgrcmk')

def query_GHG_country(df,GHG_option):
    country_name = GHG_option

    df = df.groupby(["year","country"])['value'].sum()
    df = df.reset_index()
    dfs = {country: df[df["country"] == country] for country in country_name}
    fig = go.Figure()
    for country, df in dfs.items():
        fig = fig.add_trace(go.Scatter(x=df["year"], y=df["value"], name=country))
    st.plotly_chart(fig)

if(result == True):
    st.header("You selected: {}".format(", ".join(GHG_option)))
    st.caption("Line chart displaying Greenhouse Gas Emission trends in different countries from 1990-2014.")
    query_GHG_country(ghg_df,GHG_option)
