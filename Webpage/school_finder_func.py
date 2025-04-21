import pandas as pd
from sklearn.neighbors import BallTree

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

X = data[['GIS_Lat', 'GIS_Long']].values
tree = BallTree(X, leaf_size=2)


def find_nearest_schools(suburb_name, k=3):
    # Find the suburb latitude and longitude
    suburb = data[data['Towns/suburb'] == suburb_name].iloc[0]
    suburb_lat, suburb_lon = suburb['suburb_Latitude'], suburb['suburb_longitude']

    # Query the BallTree for the k-nearest schools
    _, idxs = tree.query([[suburb_lat, suburb_lon]], k=5)
    nearest_schools = data.iloc[idxs[0]][['Official_Institution_Name']]

    # Add a number to each school
    numbered_schools = []
    for i, school in enumerate(nearest_schools['Official_Institution_Name']):
        numbered_schools.append(f"{i + 1}. {school}")

    return numbered_schools



