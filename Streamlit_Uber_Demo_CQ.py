import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

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
st.bar_chart(hist_values)
st.area_chart(hist_values)

# Plot ALL the Uber pickup data on a map of New York

st.subheader('Map of all pickups')
st.map(data)

# Plot only the data at 17:00 on a map of New York
hour_to_filter = 17
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)

# Use a slider to adjust time window then 
# plot the ride data on a map of New York
hour_to_filter = st.slider('hour', 0, 23, 17) # minimum = 0, max = 23:00, default = 17:00
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)


# Trying a random 3D hexagon histogram on dynamic map
# Reference:
# https://docs.streamlit.io/en/stable/api.html#streamlit.pydeck_chart
st.subheader('A random dynamic 3D map with hexagon histogram ')
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



