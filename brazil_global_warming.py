import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Environment Dashboard",
    page_icon="random",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title('Global Warming Trends in Different Countries')
data = pd.read_csv("archive/ENVIRON_DATA.csv")

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
  