import pandas as pd
import folium
import streamlit as st
from streamlit_folium import st_folium

def create_region_map(data, selected_region):
    # Filter the data to include only renewable energy types
    renewable_types = ['Solaire', 'Hydraulique', 'Eolien', 'Bioénergies', 'Energies Marines', 'Géothermie']
    renewable_df = data[data['filiere'].isin(renewable_types)]

    # Filter for the selected region
    if selected_region != "All":
        renewable_df = renewable_df[renewable_df['region'] == selected_region]

    # Aggregate the renewable energy data by region, summing the annual energy injected
    renewable_energy_by_region = renewable_df.groupby('region')['energieAnnuelleGlissanteInjectee'].sum().reset_index()

    # Create a map centered around France
    renewable_map = folium.Map(location=[46.603354, 1.888334], zoom_start=5)

    # Define mock locations for demonstration purposes
    location_map = {
        'Île-de-France': [48.8566, 2.3522],
        'Provence-Alpes-Côte d\'Azur': [43.9352, 6.0679],
        'Brittany': [48.1173, -1.6778],
        'Corse': [42.0396, 9.0129],
        'Auvergne-Rhône-Alpes': [45.7640, 4.8357],
        'Bourgogne-Franche-Comté': [47.2805, 5.9993],
        'Centre-Val de Loire': [47.7516, 1.6751],
        'Grand Est': [48.5734, 7.7521],
        'Hauts-de-France': [50.6292, 3.0573],
        'Normandy': [49.1829, -0.3707],
        'Nouvelle-Aquitaine': [44.8378, -0.5792],
        'Occitanie': [43.6047, 1.4442],
        'Pays de la Loire': [47.2184, -1.5536],
        'Guadeloupe': [16.2650, -61.5500],
        'Martinique': [14.6415, -61.0242],
        'Guyane': [4.9224, -52.3260],
        'La Réunion': [-21.1151, 55.5364],
        'Mayotte': [-12.8275, 45.1662]
    }

    # Add markers to the map
    for _, row in renewable_energy_by_region.iterrows():
        location = location_map.get(row['region'], [46.603354, 1.888334])
        folium.CircleMarker(
            location=location,
            radius=10,
            popup=f"{row['region']}: {row['energieAnnuelleGlissanteInjectee']} MWh",
            color="green",
            fill=True,
            fill_color="green"
        ).add_to(renewable_map)

    # Return the map object
    return renewable_map

# Streamlit app code
def main():
    st.title("Renewable Energy Usage in France")

    # Load the dataset
    data_file = 'cleaned_data.csv'  # Update with the actual path to your data file
    data = pd.read_csv(data_file)

    # List of unique regions plus an option for "All"
    regions = ["All"] + sorted(data['region'].dropna().unique().tolist())

    # Region selection menu
    selected_region = st.selectbox("Select a region to view", regions)

    # Generate the map for the selected region
    region_map = create_region_map(data, selected_region)

    # Display the map using Streamlit
    st_data = st_folium(region_map, width=700)

if __name__ == "__main__":
    main()
