import streamlit as st
from streamlit_folium import folium_static
import pandas as pd


# --- Load the dataframe ---
df = pd.read_csv(r'../../../Desktop/Data projects/Project 2/Webpage/new_df1.csv')

st.set_page_config(
    page_title="School Finder App",
    page_icon=":student:",
    layout="wide",
    initial_sidebar_state="expanded",
)


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
folium_static(map, width=1400, height=300)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

