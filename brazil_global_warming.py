import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle

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

st.dataframe(updated_data)
st.caption("Dataframe displaying temperature difference of different countries.")
country_list = updated_data.Area.values.tolist()

def query_country(df, name):
    df2 = df.query(f"Area == '{name}'")
    df2 = df2.T
    df2 = df2.rename_axis("Year")
    df2 = df2.rename(columns= lambda x: "Temp Change")
    df2 = df2.reset_index(drop=False)
    df2 = df2[1:]
    
    return df2

option = st.selectbox('Choose a country to see the global warming trend:',country_list)


#brazil_stats = query_country(updated_data,"Brazil")
country_stats = query_country(updated_data,option)

st.line_chart(country_stats,x="Year",y="Temp Change")
st.caption("Line chart displaying temperature difference of different countries from 1961-2019.")

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

st.bar_chart(deforest_stats, x='Year',y='Deforestation')
st.caption("Bar chart displaying deforestation trends across the world at different time periods up until 2015.")


ghg_df = ghg_df.rename(columns={"country_or_area": "country"})
GHG_countries = ghg_df.country.unique().tolist()
GHG_option = st.select('Choose a country to view the GHG emissions in million metric tons from 1990-2014',GHG_countries)

cycol = cycle('bgrcmk')

def query_GHG_country(df,GHG_option):
    country_name = GHG_option

    queried_df = df.query(f"country == '{country_name}'")
    queried_df = queried_df.groupby(["year"])['value'].sum()
    queried_df = queried_df.reset_index()
    y = queried_df.value
    x = queried_df.year
    #fig, ax = plt.subplots()
    #ax.plot(x,y,color=next(cycol))
    #ax.set_title("GHG Emissions per Year")
    #ax.set_xlabel("Year")
    #ax.set_ylabel("Total Greenhouse Gas Emissions (GHG)")
    st.line_chart(x,y)
query_GHG_country(ghg_df,GHG_option)