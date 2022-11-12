import streamlit as st
import pandas as pd
import numpy as np
#import plotly.express as px

st.title('Global Warming Trends in Brazil')
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


def query_country(df, name):
    df2 = df.query(f"Area == '{name}'")
    df2 = df2.T
    df2 = df2.rename_axis("Year")
    df2 = df2.rename(columns= lambda x: "Temp Change")
    df2 = df2.reset_index(drop=False)
    df2 = df2[1:]
    
    return df2

brazil_stats = query_country(updated_data,"Brazil")

st.line_chart(brazil_stats,x="Year",y="Temp Change")
