import pandas as pd
import numpy as np
import streamlit as st

def clean_data(data):
    data = data.dropna(axis=1, how='all')
    
    # Drop columns with more than 90% missing values
    cleaned_data = data.dropna(thresh=0.9*len(data), axis=1)

    for col in cleaned_data.columns:
        if 'date' in col.lower():
            cleaned_data[col] = pd.to_datetime(cleaned_data[col], dayfirst=True)

    cleaned_data.to_csv('cleaned_data.csv', index=False)
    return cleaned_data
