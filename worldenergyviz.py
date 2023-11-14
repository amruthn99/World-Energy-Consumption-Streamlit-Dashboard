import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# set the page to wide mode
st.set_page_config(layout="wide")

# load in energy data
energy_df = pd.read_csv('C:\\Users\\itsam\\Desktop\\Portfolio Projects\\owid-energy-data.csv')

# get only columns relating to energy consumption
consumption_columns = [col for col in energy_df.columns if col.endswith('_consumption')]

# sort consumptions amounts to find the most used energy sources
total_consumption = energy_df[consumption_columns].sum().sort_values(ascending=False)

# retrive top 6 energy sources
top_consumptions = total_consumption.index[1:7].tolist()

# filter for relevant columns
selected_columns = ['iso_code', 'country', 'year', 'gdp', 'population'] + top_consumptions
top_energy_df = energy_df[selected_columns]

top_energy_df = top_energy_df[top_energy_df['year']>=1990]
top_energy_df = top_energy_df[top_energy_df['year']<=2018]

countries = ['United Kingdom', 'United States', 'Germany', 'France', 'India', 'Japan']
top_energy_df = top_energy_df.loc[top_energy_df['country'].isin(countries)]

viz_df = top_energy_df

# Function to plot the data as a line chart
def plot_data(selected_country, selected_consumption, start_year, end_year):
    # Filter data based on selected country and year range
    country_data = viz_df[(viz_df['country'] == selected_country) & 
                          (viz_df['year'] >= start_year) & 
                          (viz_df['year'] <= end_year)]

    # Plotting the trend
    plt.figure(figsize=(10, 6))  # Set the figure size here
    plt.plot(country_data['year'], country_data[selected_consumption], marker='o')
    plt.title(f'{selected_consumption} trend in {selected_country} ({start_year}-{end_year})')
    plt.xlabel('Year')
    plt.ylabel(selected_consumption)
    plt.grid(True)
    return plt

# Function to create and display a pie chart of consumption percentages
def plot_consumption_pie_chart(selected_country, start_year, end_year):
    # Filter data for the selected country and year range
    country_data = viz_df[(viz_df['country'] == selected_country) & 
                          (viz_df['year'] >= start_year) & 
                          (viz_df['year'] <= end_year)]

    # Calculating total consumption for each type
    total_by_type = country_data[['fossil_fuel_consumption', 'oil_consumption', 'coal_consumption', 
                                  'gas_consumption', 'low_carbon_consumption', 'renewables_consumption']].sum()
    
    # Pie chart
    plt.figure(figsize=(10, 6))  # Ensure the figure size is the same as the line chart
    plt.pie(total_by_type, labels=total_by_type.index, autopct='%1.1f%%', startangle=140)
    plt.title(f'Consumption Breakdown in {selected_country} ({start_year}-{end_year})')
    return plt

# Streamlit app
st.title('World Energy Consumption Trends Dashboard')

# Year range selection
years = sorted(viz_df['year'].unique())
start_year, end_year = st.select_slider(
    'Select Year Range',
    options=years,
    value=(years[0], years[-1])
)

# Creating two columns for the country and consumption type selection
col1, col2 = st.columns(2)

# Country selection in the first column
with col1:
    country_list = viz_df['country'].unique()
    selected_country = st.selectbox('Select a Country', country_list)

# Consumption type selection in the second column
with col2:
    consumption_types = ['fossil_fuel_consumption', 'oil_consumption', 'coal_consumption', 
                         'gas_consumption', 'low_carbon_consumption', 'renewables_consumption']
    selected_consumption = st.selectbox('Select Consumption Type', consumption_types)

# Creating two columns for the pie chart and the line chart
col1, col2 = st.columns(2)

# Display the pie chart in the first column
with col1:
    pie_chart = plot_consumption_pie_chart(selected_country, start_year, end_year)
    st.pyplot(pie_chart)

# Display the line chart in the second column
with col2:
    line_chart = plot_data(selected_country, selected_consumption, start_year, end_year)
    st.pyplot(line_chart)
