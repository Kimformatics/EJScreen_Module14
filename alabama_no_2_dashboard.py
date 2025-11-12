import pandas as pd
import plotly.express as px
import streamlit as st

# Load Data
df = pd.read_csv('alabamaData2024_NO2.csv')

# Streamlit App Title
st.title('Alabama NO₂ Air Quality Dashboard (2024)')

# Sidebar Filters
st.sidebar.header('Filter Data')
counties = st.sidebar.multiselect('Select County:', sorted(df['COUNTY'].unique()))
date_range = st.sidebar.date_input('Select Date Range:', [])

# Filter Data Based on Selections
filtered_df = df.copy()
if counties:
    filtered_df = filtered_df[filtered_df['COUNTY'].isin(counties)]
if date_range:
    filtered_df = filtered_df[(pd.to_datetime(filtered_df['Date']) >= pd.to_datetime(date_range[0])) & 
                              (pd.to_datetime(filtered_df['Date']) <= pd.to_datetime(date_range[-1]))]

# Summary Statistics
st.subheader('Summary Statistics')
st.write(filtered_df.describe(include='all'))

# Time Series Plot
st.subheader('NO₂ Concentration Over Time')
fig_time = px.line(filtered_df, x='Date', y='Daily_Mean_PM2_5_Concentration', color='COUNTY',
                   labels={'Daily_Mean_PM2_5_Concentration': 'Mean NO₂ (µg/m³)', 'Date': 'Date'},
                   title='NO₂ Concentrations Over Time by County')
st.plotly_chart(fig_time)

# Geographic Distribution
st.subheader('Geographic Distribution of NO₂ Levels')
fig_map = px.scatter_mapbox(filtered_df, lat='SITE_LATITUDE', lon='SITE_LONGITUDE', color='Daily_Mean_PM2_5_Concentration',
                            hover_name='Site_Name', size='Daily_Mean_PM2_5_Concentration', zoom=6,
                            color_continuous_scale='Reds', height=500, mapbox_style='carto-positron',
                            title='NO₂ Monitoring Sites and Concentrations')
st.plotly_chart(fig_map)

# AQI Distribution by County
st.subheader('AQI Distribution by County')
fig_aqi = px.box(filtered_df, x='COUNTY', y='DAILY_AQI_VALUE', color='COUNTY',
                 labels={'DAILY_AQI_VALUE': 'Daily AQI Value', 'COUNTY': 'County'},
                 title='Distribution of AQI by County')
st.plotly_chart(fig_aqi)

# Download Filtered Data
st.subheader('Download Filtered Dataset')
st.download_button('Download CSV', filtered_df.to_csv(index=False).encode('utf-8'), 'filtered_alabama_NO2_data.csv', 'text/csv')
