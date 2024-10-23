import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data
def clean_data(df):
    #drop the columns that are feeled with null values
    df.dropna(axis=1, inplace=True)
    #fill the null values with the mean of the column
    df.fillna(df.mean(), inplace=True)
    pd.to_datetime(df['date'])
    
    return df