import base64
from flask import Flask, render_template, send_file
import matplotlib.pyplot as plt
import io
from map_creation import create_interactive_map, get_data_for_region
from flask import Flask, render_template, request
from flask import Flask, render_template, jsonify, request, session, send_file
import os
from flask import session, redirect, url_for, render_template
import geopandas as gpd
import pandas as pd
import plotly.graph_objects as go
app = Flask(__name__)
app.secret_key = os.urandom(24)

import streamlit as st
import sys

python_version = sys.version
st.write("Python version used by this Streamlit app:", python_version)
@app.route('/')
def index():
    # Generate the map when the index page is loaded
    return render_template('MILL.html')

@app.route('/map', methods=['POST'])
def map():
    # Access the form data from the query parameters
    demographic_category = request.form.get('demographicCategory')
    region = request.form.get('region')
    data_level = request.form.get('dataLevel')
    print(demographic_category)
    print(region)
    print(data_level)
   
    if region=='Greater Manchester':
        folder='GM'
        if data_level=='LSOA':
            LevelPath='Boundaries-20240419T224611Z-001/Boundaries/GM_Boundaries/GM_LSOAs/GM_LSOAs.shp'
            code='code'
            if demographic_category=='Number of usual residents':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts001/census2021-ts001-lsoa-filtered.csv'
            elif demographic_category=='Legal partnership status':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts002/census2021-ts002-lsoa-filtered.csv'
            elif demographic_category=='Household composition':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts003/census2021-ts003-lsoa-filtered.csv'
            
            elif demographic_category=='Passports held':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts005/census2021-ts005-lsoa-filtered.csv'
            elif demographic_category=='Population density':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts006/census2021-ts006-lsoa-filtered.csv'
            
            elif demographic_category=='Sex':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts008/census2021-ts008-lsoa-filtered.csv'
            
            elif demographic_category=='Household Deprivation':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts011/census2021-ts011-lsoa-filtered.csv'
            elif demographic_category=='Year of arrival in UK':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts015/census2021-ts015-lsoa-filtered.csv'
            elif demographic_category=='Length of residence':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts016/census2021-ts016-lsoa-filtered.csv'
            elif demographic_category=='Household size':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts017/census2021-ts017-lsoa-filtered.csv'
            elif demographic_category=='Age of arrival in the UK':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts018/census2021-ts018-lsoa-filtered.csv'
            elif demographic_category=='Migrant Indicator':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts019/census2021-ts019-lsoa-filtered.csv'
            elif demographic_category=='Number of non-UK short-term residents by sex':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts020/census2021-ts020-lsoa-filtered.csv'
            elif demographic_category=='Ethnic Group':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts021/census2021-ts021-lsoa-filtered.csv'
            elif demographic_category=='Number of Households':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts041/census2021-ts041-lsoa-filtered.csv'
            else:
                print('No Demographic data selected')
        elif data_level=='MSOA':
            LevelPath='Boundaries-20240419T224611Z-001/Boundaries/GM_Boundaries/GM_MSOAs/GM_MSOAs.shp'
            code='msoa21cd'
            if demographic_category=='Number of usual residents':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts001/census2021-ts001-msoa-filtered.csv'
            elif demographic_category=='Legal partnership status':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts002/census2021-ts002-msoa-filtered.csv'
            elif demographic_category=='Household composition':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts003/census2021-ts003-msoa-filtered.csv'
           
            elif demographic_category=='Passports held':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts005/census2021-ts005-msoa-filtered.csv'
            elif demographic_category=='Population density':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts006/census2021-ts006-msoa-filtered.csv'
           
            elif demographic_category=='Sex':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts008/census2021-ts008-msoa-filtered.csv'
            
            elif demographic_category=='Household Deprivation':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts011/census2021-ts011-msoa-filtered.csv'
            elif demographic_category=='Year of arrival in UK':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts015/census2021-ts015-msoa-filtered.csv'
            elif demographic_category=='Length of residence':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts016/census2021-ts016-msoa-filtered.csv'
            elif demographic_category=='Household size':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts017/census2021-ts017-msoa-filtered.csv'
            elif demographic_category=='Age of arrival in the UK':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts018/census2021-ts018-msoa-filtered.csv'
            elif demographic_category=='Migrant Indicator':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts019/census2021-ts019-msoa-filtered.csv'
            elif demographic_category=='Number of non-UK short-term residents by sex':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts020/census2021-ts020-msoa-filtered.csv'
            elif demographic_category=='Ethnic Group':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts021/census2021-ts021-msoa-filtered.csv'
            elif demographic_category=='Number of Households':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts041/census2021-ts041-msoa-filtered.csv'
            
            else:
                print('No Demographic data selected')
        elif data_level=='LTLA':
            LevelPath='Boundaries-20240419T224611Z-001/Boundaries/GM_Boundaries/GM_LAs/GM.shp'
            code='geo_code'
            if demographic_category=='Number of usual residents':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts001/census2021-ts001-ltla-filtered.csv'
            elif demographic_category=='Legal partnership status':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts002/census2021-ts002-ltla-filtered.csv'
            elif demographic_category=='Household composition':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts003/census2021-ts003-ltla-filtered.csv'
           
            elif demographic_category=='Passports held':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts005/census2021-ts005-ltla-filtered.csv'
            elif demographic_category=='Population density':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts006/census2021-ts006-ltla-filtered.csv'
            
            elif demographic_category=='Sex':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts008/census2021-ts008-ltla-filtered.csv'
            
            elif demographic_category=='Household Deprivation':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts011/census2021-ts011-ltla-filtered.csv'
            elif demographic_category=='Year of arrival in UK':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts015/census2021-ts015-ltla-filtered.csv'
            elif demographic_category=='Length of residence':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts016/census2021-ts016-ltla-filtered.csv'
            elif demographic_category=='Household size':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts017/census2021-ts017-ltla-filtered.csv'
            elif demographic_category=='Age of arrival in the UK':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts018/census2021-ts018-ltla-filtered.csv'
            elif demographic_category=='Migrant Indicator':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts019/census2021-ts019-ltla-filtered.csv'
            elif demographic_category=='Number of non-UK short-term residents by sex':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts020/census2021-ts020-ltla-filtered.csv'
            elif demographic_category=='Ethnic Group':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts021/census2021-ts021-ltla-filtered.csv'
            elif demographic_category=='Number of Households':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts041/census2021-ts041-ltla-filtered.csv'
            
            else:
                print('No Demographic data selected')
        elif data_level=='UTLA':
            LevelPath='Boundaries-20240419T224611Z-001/Boundaries/GM_Boundaries/GM_OAs/GM_OAs.shp'
    elif region=='West Midlands':
        if data_level=='LSOA':
            LevelPath='Boundaries-20240419T224611Z-001/Boundaries/WM_Boundaries/WM_LSOAs/WM_LSOAs.shp'
            code='lsoa21cd'
            if demographic_category=='Number of usual residents':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts001/census2021-ts001-lsoa-filtered.csv'
            elif demographic_category=='Legal partnership status':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts002/census2021-ts002-lsoa-filtered.csv'
            elif demographic_category=='Household composition':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts003/census2021-ts003-lsoa-filtered.csv'
            
            elif demographic_category=='Passports held':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts005/census2021-ts005-lsoa-filtered.csv'
            elif demographic_category=='Population density':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts006/census2021-ts006-lsoa-filtered.csv'
            
            elif demographic_category=='Sex':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts008/census2021-ts008-lsoa-filtered.csv'
            
            elif demographic_category=='Household Deprivation':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts011/census2021-ts011-lsoa-filtered.csv'
            elif demographic_category=='Year of arrival in UK':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts015/census2021-ts015-lsoa-filtered.csv'
            elif demographic_category=='Length of residence':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts016/census2021-ts016-lsoa-filtered.csv'
            elif demographic_category=='Household size':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts017/census2021-ts017-lsoa-filtered.csv'
            elif demographic_category=='Age of arrival in the UK':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts018/census2021-ts018-lsoa-filtered.csv'
            elif demographic_category=='Migrant Indicator':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts019/census2021-ts019-lsoa-filtered.csv'
            elif demographic_category=='Number of non-UK short-term residents by sex':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts020/census2021-ts020-lsoa-filtered.csv'
            elif demographic_category=='Ethnic Group':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts021/census2021-ts021-lsoa-filtered.csv'
            elif demographic_category=='Number of Households':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts041/census2021-ts041-lsoa-filtered.csv'
            else:
                print('No Demographic data selected')
        elif data_level=='MSOA':
            LevelPath='Boundaries-20240419T224611Z-001/Boundaries/WM_Boundaries/WM_MSOAs/WM_MSOAs.shp'
            code='msoa21cd'
            if demographic_category=='Number of usual residents':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts001/census2021-ts001-msoa-filtered.csv'
            elif demographic_category=='Legal partnership status':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts002/census2021-ts002-msoa-filtered.csv'
            elif demographic_category=='Household composition':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts003/census2021-ts003-msoa-filtered.csv'
            
            elif demographic_category=='Passports held':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts005/census2021-ts005-msoa-filtered.csv'
            elif demographic_category=='Population density':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts006/census2021-ts006-msoa-filtered.csv'
            
            elif demographic_category=='Sex':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts008/census2021-ts008-msoa-filtered.csv'
            
            elif demographic_category=='Household Deprivation':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts011/census2021-ts011-msoa-filtered.csv'
            elif demographic_category=='Year of arrival in UK':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts015/census2021-ts015-msoa-filtered.csv'
            elif demographic_category=='Length of residence':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts016/census2021-ts016-msoa-filtered.csv'
            elif demographic_category=='Household size':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts017/census2021-ts017-msoa-filtered.csv'
            elif demographic_category=='Age of arrival in the UK':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts018/census2021-ts018-msoa-filtered.csv'
            elif demographic_category=='Migrant Indicator':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts019/census2021-ts019-msoa-filtered.csv'
            elif demographic_category=='Number of non-UK short-term residents by sex':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts020/census2021-ts020-msoa-filtered.csv'
            elif demographic_category=='Ethnic Group':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts021/census2021-ts021-msoa-filtered.csv'
            elif demographic_category=='Number of Households':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts041/census2021-ts041-msoa-filtered.csv'
            
            else:
                print('No Demographic data selected')
        elif data_level=='LTLA':
            LevelPath='Boundaries-20240419T224611Z-001/Boundaries/WM_Boundaries/WM_LAs/WM_LAs.shp'
            code='ltla22cd'
            if demographic_category=='Number of usual residents':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts001/census2021-ts001-ltla-filtered.csv'
            elif demographic_category=='Legal partnership status':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts002/census2021-ts002-ltla-filtered.csv'
            elif demographic_category=='Household composition':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts003/census2021-ts003-ltla-filtered.csv'
            
            elif demographic_category=='Passports held':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts005/census2021-ts005-ltla-filtered.csv'
            elif demographic_category=='Population density':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts006/census2021-ts006-ltla-filtered.csv'
            
            elif demographic_category=='Sex':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts008/census2021-ts008-ltla-filtered.csv'
            
            elif demographic_category=='Household Deprivation':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts011/census2021-ts011-ltla-filtered.csv'
            elif demographic_category=='Year of arrival in UK':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts015/census2021-ts015-ltla-filtered.csv'
            elif demographic_category=='Length of residence':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts016/census2021-ts016-ltla-filtered.csv'
            elif demographic_category=='Household size':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts017/census2021-ts017-ltla-filtered.csv'
            elif demographic_category=='Age of arrival in the UK':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts018/census2021-ts018-ltla-filtered.csv'
            elif demographic_category=='Migrant Indicator':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts019/census2021-ts019-ltla-filtered.csv'
            elif demographic_category=='Number of non-UK short-term residents by sex':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts020/census2021-ts020-ltla-filtered.csv'
            elif demographic_category=='Ethnic Group':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts021/census2021-ts021-ltla-filtered.csv'
            elif demographic_category=='Number of Households':
                level='Collective_Census_2021_folder_filtered-20240419T224609Z-001/Collective_Census_2021_folder_filtered/census2021-ts041/census2021-ts041-ltla-filtered.csv'
            
            else:
                print('No Demographic data selected')
        elif data_level=='UTLA':
            LevelPath='Boundaries-20240419T224611Z-001/Boundaries/WM_Boundaries/WM_OAs/WM_OAs.shp'
    base_dir = os.path.dirname(__file__)  # Get the directory where the script runs
    level = os.path.join(base_dir, level)
    LevelPath = os.path.join(base_dir, LevelPath)
    
    print(level)
    print(LevelPath)
    session['level'] = level
    session['LevelPath'] = LevelPath
    session['code'] = code
    # Assuming map_folium is a variable containing data you want to pass
    #session['map_data'] = map_folium._repr_html_()  # Store the map's HTML representation in the session

    # Redirect to a new page that will render the map
    return jsonify({'redirect': url_for('show_map')})
def calculate_region_stats(merged_gdf, indicator_column):
    # Calculate minimum, maximum, and average
    min_value = merged_gdf[indicator_column].min()
    max_value = merged_gdf[indicator_column].max()
    avg_value = merged_gdf[indicator_column].mean()

    # Get the region(s) with min and max values
    min_region = merged_gdf[merged_gdf[indicator_column] == min_value]['geography'].iloc[0]
    max_region = merged_gdf[merged_gdf[indicator_column] == max_value]['geography'].iloc[0]

    # Create a dictionary to return the results
    stats = {
        "labels": ["Minimum", "Average", "Maximum"],
        "values": [min_value, avg_value, max_value],
        "regions": [min_region, "Average", max_region]
    }
    
    return stats

@app.route('/show_map')
def show_map():
    # Retrieve the map data from the session
    level = session.get('level')
    LevelPath = session.get('LevelPath')
    code=session.get('code')
    map_folium= create_interactive_map(LevelPath, level, code, 'geography code', ['date', 'geography'])
    map_html = map_folium._repr_html_() if map_folium else ""
    gdf = gpd.read_file(LevelPath)
    csv_data = pd.read_csv(level)
    csv_data['geography code'] = csv_data['geography code'].astype(str)
    gdf[code] = gdf[code].astype(str)
    merged_gdf = gdf.merge(csv_data, left_on=code, right_on='geography code', how='inner')
    # Render the MapWithHTML template with the map data
    data_for_classification = csv_data.columns[3]
    stats = calculate_region_stats(merged_gdf, data_for_classification)
    keyval=data_for_classification.split(':')[0]
    # Create the Plotly figure
    fig = go.Figure([go.Bar(x=stats['regions'], y=stats['values'], text=stats['values'], textposition='auto', marker_color='#db0a5b')])

    fig.update_layout(
        title=f'Summary Statistics for {keyval}',
        xaxis_tickangle=-90,
        xaxis_title='Region',
        yaxis_title='Value',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    # Convert plotly figure to HTML
    graph_html = fig.to_html(full_html=False)
    return render_template('MapWithHTML.html', map_data=map_html, graph_html=graph_html)

@app.route('/download_chart/<region_id>')
def download_chart(region_id):
    exclude_columns = ['date', 'geography code', 'geography']
    level = session.get('level')
    LevelPath = session.get('LevelPath')
    code=session.get('code')
    region_data = get_data_for_region(level, LevelPath,code, region_id, exclude_columns)
    if region_data:
        buffer = generate_chart(region_data)
        buffer.seek(0)
        img_str = base64.b64encode(buffer.read()).decode('utf-8')
        return jsonify({'img_data': 'data:image/png;base64,' + img_str})
    else:
        return jsonify({'error': 'No data available for the requested region.'}), 404

def generate_chart(data):
    # Here, you generate the chart using matplotlib
    labels = [key.split(': ')[1].split(';')[0] for key in data.keys()]
    values = list(data.values())
    label = [key.split(':')[0] for key in data.keys()]
    print(labels)
    # Calculate statistics
    
    maxvals=[]
    for key, value in data.items():
        if 'Total' not in key:  # Check if 'Total' is not in the column name
            # Extracting the part of the label after ': ' and before ';', if present
            
            maxvals.append(value)
    plt.switch_backend('Agg')
    buf = io.BytesIO()
    min_value = min(values)
    max_value = max(maxvals)
    avg_value = sum(maxvals) / len(maxvals)
    plt.figure(figsize=(8, 4))  # Aspect ratio 2:1, for example

    bars = plt.bar(labels, values, color='#db0a5b')

    # Highlight the min and max bars
    bars[values.index(min_value)].set_color('#fec5af')  # Color the min value bar
    bars[values.index(min_value)].set_label('Min Value')
    bars[values.index(max_value)].set_color('#f4979a')  # Color the max value bar
    bars[values.index(max_value)].set_label('Max Value')

    # Add a horizontal line for the average
    plt.axhline(y=avg_value, color='k', linestyle='--', linewidth=1)
    
    # Add legend for the min and max
    plt.legend(loc='upper right')

    plt.title(label[0])
    plt.xticks(rotation=90)
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()  # Close the figure to free memory
    buf.seek(0)
    return buf

if __name__ == '__main__':
    #app.run(debug=True, threaded=False)
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 9000)))
  
