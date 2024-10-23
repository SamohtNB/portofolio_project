import pandas as pd
import numpy as np
import streamlit as st

def clean_data(data):
    data = data.dropna(axis=1, how='all')
    
    cleaned_data = data.drop(columns=['codeEICResourceObject', 'codeIRIS', 'codeINSEECommune',
        'codeEPCI', 'codeIRISCommuneImplantation',
        'codeINSEECommuneImplantation', 'codeS3RENR'])
    for col in cleaned_data.columns:
        if 'date' in col.lower():
            cleaned_data[col] = pd.to_datetime(cleaned_data[col], errors='coerce')

    # Automatically convert numeric columns to the appropriate type
    numeric_columns = cleaned_data.select_dtypes(include=['object']).columns
    for col in numeric_columns:
        # Attempt to convert to numeric, if conversion fails it remains as object
        cleaned_data[col] = pd.to_numeric(cleaned_data[col], errors='coerce')

