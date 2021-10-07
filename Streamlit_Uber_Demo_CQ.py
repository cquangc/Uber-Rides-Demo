import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from scipy.stats import norm

# Acknowledgements
# This is adapted from 
#https://docs.streamlit.io/en/stable/tutorial/create_a_data_explorer_app.html
# Accessed 7 October 2021, currently available

# Create app title for browser
st.title('Cuongs Uber pickups in NYC Streamlit demo')

# Fetch Uber data

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
#data_load_state.text('Loading data...done!')
data_load_state.text("Done! (using st.cache)")

#Display the data in the webapp if selected with a check box
st.subheader('Raw data')
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)


#Draw a histogram of the data
st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

# Try different plotting methods
st.subheader('Histogram')
st.bar_chart(hist_values)
st.subheader('Area Chart')
st.area_chart(hist_values)

# Plot ALL the Uber pickup data on a map of New York

st.subheader('Map of all pickups')
st.subheader('Hold shift to orbit, scroll to zoom')
st.map(data)

# Plot only the data at 17:00 on a map of New York
hour_to_filter = 17
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.subheader('Hold shift to orbit, scroll to zoom')
st.map(filtered_data)

# Use a slider to adjust time window then 
# plot the ride data on a map of New York
hour_to_filter = st.slider('hour', 0, 23, 17) # minimum = 0, max = 23:00, default = 17:00
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.subheader('Hold shift to orbit, scroll to zoom')
st.map(filtered_data)


# Trying a random 3D hexagon histogram on static map
# Reference:
# https://docs.streamlit.io/en/stable/api.html#streamlit.pydeck_chart
st.subheader('A random 3D map with hexagon histogram ')
df = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4], columns=['lat', 'lon'])
st.pydeck_chart(pdk.Deck(
map_style='mapbox://styles/mapbox/light-v9',
initial_view_state=pdk.ViewState(
	latitude=37.76,
	longitude=-122.4,
	zoom=11,
	pitch=50,
	),
	layers=[
			pdk.Layer(
			'HexagonLayer',
			data=df,
			get_position='[lon, lat]',
			radius=200,
			elevation_scale=4,
			elevation_range=[0, 1000],
			pickable=True,
			extruded=True,
			),
	pdk.Layer(
			'ScatterplotLayer',
			data=df,
			get_position='[lon, lat]',
			get_color='[200, 30, 0, 160]',
			get_radius=200,
			),
	],
))

# A plot with integrated sliders
st.subheader('A plot with integrated sliders')
x = np.arange(-3, 3, 0.001)
mu = st.slider('mu', min_value = 0.0, max_value = 1.0, value = 0.5) # minimum = 0, max = 1, default = 0.5
sd = st.slider('sd', min_value = 0.0, max_value = 1.0, value = 0.5) # minimum = 0, max = 1, default = 0.5
y = norm.pdf(x, mu, sd)
st.area_chart(y)

st.subheader('About this app')
st.write('This is a simple demo to demonstrate how easy it is to produce a webapp entirely in Python \n')
st.write('We will access raw data stored in an AWS S3 repository on Uber rides in New York \n')
st.write('We will then visualise these data in various static and dynamic charts \n')
st.write('The webapp also incorporates several widgets to demonstrate the potential for interactivity \n')
st.write('such as radio buttons and slider bars. \n')
st.write('The webapp employs the use of data caching with state awareness to mitigate the need to constantly refresh data pulls from S3 each time it is invoked. This saves time for the user as well as reducing the load on S3. \n')
st.write('The code resides in GitHub as a public .py script \n')
st.write('A requirements.txt file in the repo contains the additional requirements that are outside the usual python libraries. \n')
st.write('In this case these are streamlit and pydeck \n')
st.write('The code is accessible by clicking on the 3 horizontal bars in the top right corner of the window. \n')
st.write('Thanks for viewing this demo! \n')





