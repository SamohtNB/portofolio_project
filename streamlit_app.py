import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import folium

from streamlit_folium import st_folium
from energy_map_creation import create_region_map
from clean_dataframe import clean_data
from create_co2_map import create_co2_map

center_css = """
    <style>
    .centered {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
    </style>
    """
    

st.set_page_config(page_title="Energy installation in France", page_icon="./image_corrigee.jpg", layout="wide")
st.markdown(center_css, unsafe_allow_html=True)


data_url = "https://www.data.gouv.fr/fr/datasets/r/c14e5a7d-2ca6-4ad8-bc61-93889d13fc25"

@st.cache_data
def load_data():
    file_path = "./cleaned_data.csv"
    if os.path.exists(file_path):
        data = pd.read_csv(file_path)
    else:
        data = pd.read_csv(data_url, sep=";", low_memory=False)
        cleaned_data = clean_data(data)
    return cleaned_data

st.sidebar.title("Menu")
page = st.sidebar.radio("Go to", ["Portfolio","Presentation","Raw data", "Data Visualization"])

data = load_data()

if page == "Presentation":
    st.title("Presentation")
    st.title("Energy installation in France")
    st.subheader("description:")
    st.markdown("""
                This project is about the energy installation in France. The data is from the french government and is updated every month.
                Energy installation in France is a very important subject because of the energy transition law that was voted in 2015.
                It is also very varied but tries to rely less and less on nuclear energy and fossile energy.
                
                here is the link to the dataset : [french gouvernement database, Registre national des installations de production et de stockage d'électricité (au 31/08/2024](https://www.data.gouv.fr/fr/datasets/registre-national-des-installations-de-production-et-de-stockage-delectricite-au-31-08-2024/)
                """, unsafe_allow_html=True)

elif page == "Raw data":
    st.title("Raw data")
    st.subheader("here is the raw data that we will be working with(we ):")
    st.write(data)
    
    st.subheader("here is the description of the data:")
    st.write(data.describe())
    
    st.subheader("here is the shape of the data:")
    st.write(data.shape)
    
    st.subheader("here is the type of the data:")
    st.write(data.dtypes)
    
    st.subheader("here are the columns of the data and what they represent:")
    st.markdown("""
        1. **nomInstallation**: Name of the electricity production or storage facility.
        2. **codeEICResourceObject**: EIC (Energy Identification Code) identifying the energy resource object.
        3. **codeIRIS**: IRIS code for the geographic location.
        4. **codeINSEECommune**: INSEE code of the municipality where the facility is located.
        5. **commune**: Name of the municipality.
        6. **codeEPCI**: Code of the Public Establishment for Inter-Municipal Cooperation (EPCI).
        7. **EPCI**: Name of the EPCI to which the municipality belongs.
        8. **codeDepartement**: Code of the department where the facility is located.
        9. **departement**: Name of the department.
        10. **codeRegion**: Code of the administrative region.
        11. **region**: Name of the region.
        12. **codeIRISCommuneImplantation**: IRIS code for the facility's location.
        13. **codeINSEECommuneImplantation**: INSEE code for the facility's implantation municipality.
        14. **codeS3RENR**: Code of the Regional Connection Scheme for Renewable Energy.
        15. **dateRaccordement**: Connection date of the facility to the electricity grid.
        16. **dateDeraccordement**: Date of disconnection from the grid, if applicable.
        17. **dateMiseEnService**: Initial commissioning date of the facility.
        18. **dateDebutVersion**: Start date of the current version of the facility.
        19. **posteSource**: Source substation to which the facility is connected.
        20. **tensionRaccordement**: Connection voltage of the facility.
        21. **modeRaccordement**: Mode of connection to the grid.
        22. **codeFiliere**: Code representing the type of energy sector (solar, wind, etc.).
        23. **filiere**: Name of the energy sector.
        24. **codeCombustible**: Code for the type of fuel used, if applicable.
        25. **combustible**: Type of fuel used in the facility.
        26. **codesCombustiblesSecondaires**: Codes for secondary fuels, if any.
        27. **combustiblesSecondaires**: Types of secondary fuels used.
        28. **codeTechnologie**: Code for the technology used in the facility.
        29. **technologie**: Type of technology used for energy production or storage.
        30. **typeStockage**: Type of energy storage (if applicable).
        31. **puisMaxInstallee**: Maximum installed power of the facility (in MW).
        32. **puisMaxRacCharge**: Maximum connection power for charging (in MW).
        33. **puisMaxCharge**: Maximum charging power of the facility (in MW).
        34. **puisMaxRac**: Maximum connection power (in MW).
        35. **puisMaxInstalleeDisCharge**: Maximum installed power for discharging (in MW).
        36. **nbGroupes**: Number of production groups within the facility.
        37. **nbInstallations**: Total number of production or storage facilities.
        38. **regime**: Operating regime of the facility.
        39. **energieStockable**: Type of energy that can be stored.
        40. **capaciteReservoir**: Storage reservoir capacity (in MWh).
        41. **hauteurChute**: Drop height for hydroelectric installations (in meters).
        42. **productible**: Amount of producible energy from the facility (in MWh).
        43. **debitMaximal**: Maximum flow rate for hydroelectric installations (in m³/s).
        44. **codeGestionnaire**: Code of the facility's manager.
        45. **gestionnaire**: Name of the facility's manager.
        46. **energieAnnuelleGlissanteInjectee**: Amount of energy injected annually into the grid (in MWh).
        47. **energieAnnuelleGlissanteProduite**: Amount of energy produced annually (in MWh).
        48. **energieAnnuelleGlissanteSoutiree**: Amount of energy withdrawn annually (in MWh).
        49. **energieAnnuelleGlissanteStockee**: Amount of energy stored annually (in MWh).
        50. **maxPuis**: Maximum power achieved by the facility (in MW).
        51. **dateMiseEnservice (format date)**: Commissioning date with a specific date format.
                """)
    
elif page == "Data Visualization":
    st.subheader("let us check for missing values:")
    # present the missing values in the data with a 
    import missingno as msno
    plt.figure(figsize=(10, 6))
    msno.matrix(data)
    st.pyplot(plt)

    st.markdown("""
                As we can see, there are a lot of missing values in the data. Either they are due to not being filled by the person in charge of the data or they are not applicable to the facility.
                """)

    
    st.subheader("let us check for the correlation between the columns containing numerical values:")
    # present the correlation between the columns of the data with a heatmap
    plt.figure(figsize=(10, 5))
    sns.heatmap(data.corr(), annot=True, cmap="viridis")
    st.pyplot(plt)
    
    st.subheader("let us check the distribution of the installed power by region:")
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='codeRegion', y='puisMaxInstallee', data=data)
    plt.xticks(rotation=90)
    plt.title('Installed Power Distribution by Region')
    plt.xlabel('Region')
    plt.ylabel('Installed Power (MW)')
    st.pyplot(plt)
    

    
    selected_region = st.selectbox("Select a region", ["All"] + data['region'].unique().tolist())
    st.subheader(f"Energy Installation in {selected_region}")
    region_map = create_region_map(data, selected_region)
    st_data = st_folium(region_map)
    

elif page == "Portfolio":
    st.title("About me")
    st.title("Hello, I\'m Thomas Masselles")
    st.image("./image_corrigee.jpg", width=200)
    st.markdown("""
                I am currently studying at EFREI to become a future data scientist.
                I have been studying data science for 2 years and programmation in general since my second year in high school.
                """)
    st.subheader("my contact informations:")
    st.markdown("""
                * email : thomas.masselles.78@gmail.com
                * linkedin : [linkedin](https://www.linkedin.com/in/thomas-masselles/)
                * cv : <a href="./CV_english_ver.pdf" target="_blank">Open PDF</a>
                """, unsafe_allow_html=True)
    st.subheader("my projects:")
    st.markdown("""
                1 the Explain project:
                * Development of a project determining the domain of a patent using python
                * Training of multiples models such as KNN and randomTree from Scikit-learn to determine the domain
                * Implementation of the user interface in a simple format taking as an input the description of a patent and giving back the determined domain and other useful informations with Streamlit 

                2 the minecraft encyclopedia project:
                * Development of a website acting as an encyclopedia centered around Minecraft with html, CSS, node.js and SQL
                * Creation of the database in SQL to store user accounts and informations
                * leading of the team in charge of the database in compliance with the other member of the group
                * Management of the interaction between server and database with node.js and the Knex library
                """)
    st.subheader("my skills:")
    st.markdown("""
                * Python
                * SQL
                * Machine learning
                * Data visualization
                * Numpy
                * Pandas
                * Scikit-learn
                * Streamlit
                * Linux
                * Git
                """, unsafe_allow_html=True)    



