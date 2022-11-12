import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title('Global Warming Trends in Brazil')
data = pd.read_csv("archive/Environment_Temperature_change_E_All_Data_NOFLAG.csv")

def preprocess_data(df):
    df = df.copy()
    df = df.query("Element == 'Temperature change'")
    df_grouped = df.groupby("Area").mean()
    df_grouped.reset_index()
    df_grouped.drop(df_grouped.columns[[0,1,2]], inplace=True, axis=1)
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

#
brazil_stats = query_country(updated_data,"Brazil")

'''option = st.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone'))

st.write('You selected:', option)
'''


#fig = px.line(brazil_stats, x="Year", y="Temp Change", labels={"Temp Change": "Change in temperature (C)"}, title= "Average Temperature Change in Brazil Over Time")
st.line_chart(brazil_stats,x="Year",y="Temp Change")
#fig.show()