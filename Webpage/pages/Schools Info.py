import streamlit as st
from sklearn.neighbors import BallTree
from streamlit_folium import folium_static
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import matplotlib.patches as patches
import matplotlib.path as path
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title="School Information", page_icon=":information:", layout="wide")

# set the title of the app
st.title("School Information")

df = pd.read_csv("Webpage/new_data.csv")

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

df['Telephone'] = df['Telephone'].apply(str)

# Create a dropdown to select an official institution name
selected_school = st.sidebar.selectbox("Select School", df["Official_Institution_Name"])

# Filter the DataFrame to include only the selected institution
filtered_df = df[df["Official_Institution_Name"] == selected_school]

# Extract relevant information from the filtered DataFrame
sector = filtered_df.iloc[0]["Sector"]
phase = filtered_df.iloc[0]["Phase_PED"]
specialisation = filtered_df.iloc[0]["Specialisation"]
telephone = filtered_df.iloc[0]["Telephone"]
address = filtered_df.iloc[0]["StreetAddress"]
fees = filtered_df.iloc[0]["School Fees"]

# --- FUNCTION THAT RETURNS SCORE CARDS ---
def plot_with_border(text_string):
    fig = plt.figure(figsize=(3, 2))
    fig.set_facecolor('silver')

    # Create a rectangle that will serve as the background
    rect = patches.Rectangle((0.05, 0.05), 0.9, 0.9, transform=fig.transFigure,
                             facecolor='white', edgecolor='none', linewidth=0)

    # Create a rounded rectangle that will serve as the border
    border_radius = 0.05
    border_path = path.Path(
        [(0, border_radius), (0, 1 - border_radius), (border_radius, 1),
         (1 - border_radius, 1), (1, 1 - border_radius), (1, border_radius),
         (1 - border_radius, 0), (border_radius, 0), (0, border_radius)])
    border_patch = patches.PathPatch(border_path, transform=fig.transFigure,
                                     facecolor='silver', edgecolor='silver',
                                     linewidth=3)

    # Add the patches to the figure
    fig.patches.extend([rect, border_patch])

    # Add the text to the figure
    text = fig.text(0.5, 0.5, text_string, color='navy',
                    ha='center', va='center', size=20)
    text.set_path_effects([path_effects.Stroke(linewidth=3, foreground='navy'),
                           path_effects.Normal()])

    # Set the axis properties and tight layout
    plt.axis('off')
    plt.tight_layout(pad=1)

    return fig


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.header("Sector")
    st.pyplot(plot_with_border(sector))

with col2:
    st.header("Phase")
    st.pyplot(plot_with_border(phase))

with col3:
    st.header("Specialisation")
    st.pyplot(plot_with_border(specialisation))

with col4:
    st.header("School Fees")
    st.pyplot(plot_with_border(fees))


# ---FUNCTION THAT RETURNS SCHOOL LOCATION ON MAP ---
def school_map(df, institution_name):
    # extract the GIS coordinates (latitude and longitude) from the filtered dataframe
    lat = filtered_df.iloc[0]['GIS_Lat']
    lon = filtered_df.iloc[0]['GIS_Long']

    # create a map object centered on the GIS coordinates
    school_map = folium.Map(location=[lat, lon], zoom_start=16)

    # add a marker to the map object at the GIS coordinates
    folium.Marker(location=[lat, lon], tooltip=institution_name).add_to(school_map)

    # return the map object
    return school_map


# --- FUNCTION THAT RETURNS ADDRESS __
def get_address(df, institution_name):
    address = df.loc[df['Official_Institution_Name'] == institution_name, 'StreetAddress'].values[0]
    return '📍 ' + address


# --- FUNCTION THAT RETURNS TELEPHONE ---

def get_telephone(df, institution_name):
    telephone = df.loc[df['Official_Institution_Name'] == institution_name, 'Telephone'].values[0]
    return '📞 ' + telephone


left_col, right_col = st.columns(2)

with left_col:
    # Create the map
    map = school_map(df, selected_school)
    # Display the map
    folium_static(map, height=300)

with right_col:
    st.title('Physical Address')
    # Get the address for the selected institution
    address = get_address(df, selected_school)
    # Display the formatted address
    st.write(address)

    st.title('Telephone')
    # Get the address for the selected institution
    telephone = get_telephone(df, selected_school)
    # Display the formatted telephone
    st.write(telephone)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)