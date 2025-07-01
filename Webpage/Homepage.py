import streamlit as st
from sklearn.utils import murmurhash
from streamlit_folium import folium_static
from streamlit_folium import st_folium
import pandas as pd 
import os

st.set_page_config(
    page_title="School Finder App",
    page_icon=":student:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Load the dataframe ---
df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'new_data.csv'))

# Split the suburb coordinates
df[['suburb_Latitude', 'suburb_longitude']] = df['suburb_coordinates'].str.split(', ', expand=True)

# remove suburb coordinates column
df = df.drop(['suburb_coordinates','Town_Suburb'], axis=1)

# Strip unwanted characters
df['suburb_Latitude'] = df['suburb_Latitude'].str[1:]
df['suburb_longitude'] = df['suburb_longitude'].str[:-1]

# Change the town coordinates datatype from object to float
df['suburb_Latitude'] = pd.to_numeric(df['suburb_Latitude'], errors='coerce')
df['suburb_longitude'] = pd.to_numeric(df['suburb_longitude'], errors='coerce')

df = df.apply(lambda x: x.str.lower() if x.dtype == "object" else x)
df = df.apply(lambda x: x.str.title() if x.dtype == "object" else x)


# set the title of the app
st.title("Pretoria School Finder")

# --- SIDEBAR ---
st.sidebar.success("Select a page above.")

# --- Main Page ---

suburbs = suburb_list = df['Towns/suburb'].unique().tolist()

from school_finder_func import find_nearest_schools

# add a text input for the suburb name
suburb = st.selectbox("Enter your town:",
         options=suburbs)

if suburb:
        # call your closest_schools function with the suburb name
        schools = find_nearest_schools(suburb)

        # check if any schools were found
        if schools:
            # display the closest schools
            st.write(f'Schools near {suburb}:')
            for school in schools:
                st.write(school)
        else:
            st.write(f'No schools were found near {suburb}.')

from maps import get_closest_schools

# Call the function to get the map
map = get_closest_schools(suburb, df)

# Display the map in the Streamlit app
st_folium(map, width=1400, height=300)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

