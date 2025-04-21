import pandas as pd
import streamlit as st
from geopy.distance import geodesic
import folium

data = pd.read_csv('Webpage/new_data.csv')

# Split the suburb coordinates
data[['suburb_Latitude', 'suburb_longitude']] = data['suburb_coordinates'].str.split(', ', expand=True)

# remove suburb coordinates column
data = data.drop(['suburb_coordinates','Town_Suburb'], axis=1)

# Strip unwanted characters
data['suburb_Latitude'] = data['suburb_Latitude'].str[1:]
data['suburb_longitude'] = data['suburb_longitude'].str[:-1]

# Change the town coordinates datatype from object to float
data['suburb_Latitude'] = pd.to_numeric(data['suburb_Latitude'], errors='coerce')
data['suburb_longitude'] = pd.to_numeric(data['suburb_longitude'], errors='coerce')

data = data.apply(lambda x: x.str.lower() if x.dtype == "object" else x)
data = data.apply(lambda x: x.str.title() if x.dtype == "object" else x)

def get_closest_schools(suburb_name, data):
    # Filter the dataframe to include only the suburb of interest
    suburb_df = data[data['Towns/suburb'] == suburb_name]

    # Get the latitude and longitude of the suburb
    suburb_lat = suburb_df.iloc[0]['suburb_Latitude']
    suburb_lon = suburb_df.iloc[0]['suburb_longitude']

    # Create a list to hold the distances between the suburb and each school
    distances = []

    # Iterate over the schools in the dataframe
    for index, row in data.iterrows():
        # Get the latitude and longitude of the school
        school_lat = row['GIS_Lat']
        school_lon = row['GIS_Long']

        # Calculate the distance between the suburb and the school
        distance = geodesic((suburb_lat, suburb_lon), (school_lat, school_lon)).km

        # Add the distance to the list
        distances.append(distance)

    # Add a new column to the dataframe with the distances
    data['Distance'] = distances

    # Sort the dataframe by distance
    closest_schools = data.sort_values(by='Distance').head(5)

    # Create a map centered on the suburb
    map = folium.Map(location=[suburb_lat, suburb_lon], zoom_start=13)

    # Add a marker for the suburb
    folium.Marker(location=[suburb_lat, suburb_lon], popup=suburb_name).add_to(map)

    # Add markers for the closest schools
    for index, row in closest_schools.iterrows():
        folium.Marker(location=[row['GIS_Lat'], row['GIS_Long']], popup=row['Official_Institution_Name']).add_to(map)

    # Return the map
    return map

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
