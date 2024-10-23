import pandas as pd
import folium

def create_co2_map(data, region):
    # Filter data for the specified region
    region_data = data[data['region'] == region]

    # Aggregate CO2 emissions data by department
    co2_by_department = region_data.groupby('departement')['co2_emissions'].sum().reset_index()

    # Create a map centered on the region
    region_map = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

    # Mock locations for departments (replace with accurate coordinates)
    department_locations = {
        'Paris': [48.8566, 2.3522],
        'Bouches-du-Rhône': [43.2965, 5.3698],
        'Ille-et-Vilaine': [48.1173, -1.6778],
        'Corse-du-Sud': [41.9260, 8.7369],
        # Add more departments as needed
    }

    # Add markers for each department
    for _, row in co2_by_department.iterrows():
        department = row['departement']
        co2 = row['co2_emissions']
        location = department_locations.get(department, [46.603354, 1.888334])  # Default to France center if not found
        
        folium.CircleMarker(
            location=location,
            radius=10,
            popup=f"{department}: {co2} tons of CO2",
            color="red",
            fill=True,
            fill_color="red"
        ).add_to(region_map)

    # Return the map object
    return region_map

# Example usage
def main():
    # Load the dataset
    data_file = 'cleaned_data.csv'  # Update with the actual path to your data file
    data = pd.read_csv(data_file)

    # Add a mock CO2 emissions column for demonstration purposes
    data['co2_emissions'] = data['energieAnnuelleGlissanteInjectee'] * 0.0002  # Example calculation

    # Specify the region to view
    selected_region = "Île-de-France"  # Replace with the desired region

    # Generate the CO2 map for the selected region
    co2_map = create_co2_map(data, selected_region)

    # Save the map to an HTML file to view in a web browser
    co2_map.save('co2_map.html')

    # To display the map in a Jupyter notebook or Streamlit, you can return the map object directly
    return co2_map

# Call the main function if running as a script
if __name__ == "__main__":
    main()
