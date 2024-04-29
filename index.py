import geopandas as gpd
import pandas as pd
import folium
from folium.features import GeoJsonTooltip
from flask import Flask, render_template, jsonify
import json
from flask import send_file
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

# Define the function to create a Folium map
def create_folium_map(shapefile_path, data_csv_path, merge_on_shapefile, merge_on_csv, exclude_columns=None):
    # Load the shapefile
    gdf = gpd.read_file(shapefile_path)

    # Load the CSV file
    csv_data = pd.read_csv(data_csv_path)

    # Merge data
    csv_data[merge_on_csv] = csv_data[merge_on_csv].astype(str)
    gdf[merge_on_shapefile] = gdf[merge_on_shapefile].astype(str)
    merged_gdf = gdf.merge(csv_data, left_on=merge_on_shapefile, right_on=merge_on_csv, how='inner')
    merged_gdf = merged_gdf.to_crs(epsg=4326)

    # Generate GeoJSON
    geojson_data = merged_gdf.to_json()

    # Create a map
    center = [merged_gdf.geometry.centroid.y.mean(), merged_gdf.geometry.centroid.x.mean()]
    m = folium.Map(location=center, zoom_start=12, tiles='cartodbpositron')
    map_html = m._repr_html_().replace('<div style="width:100%;"><div style="position:relative;width:100%;height:0;padding-bottom:60%;">', '<div id="mapid" style="width:100%; height: 600px;">')
    m.get_root().html.add_child(folium.Element('<div id="mapid" style="width: 100%; height: 100%;"></div>'))

    # Ensure this div is used as the map container
    m.get_root().html.add_child(folium.Element('<script>var map = L.map("mapid").setView([45.5236, -122.6750], 13);</script>'))

    m.save('map.html')

    folium.GeoJson(
        geojson_data,
        name='GeoData',
        tooltip=GeoJsonTooltip(fields=[col for col in csv_data.columns if col not in exclude_columns],
                               aliases=[col for col in csv_data.columns if col not in exclude_columns]),
        style_function=lambda feature: {'fillColor': 'blue', 'color': 'black', 'weight': 0.5, 'fillOpacity': 0.5}
    ).add_to(m)

    return m

@app.route('/')
def index():
    # Path to your data
    shapefile_path = 'GM_LSOAs\GM_LSOAs.shp'
    data_csv_path = 'census2021-ts044-lsoa.csv'
    exclude_columns = ['date', 'geography code', 'geography']  # example columns to exclude

    # Create map and store as HTML string
    folium_map = create_folium_map(shapefile_path, data_csv_path, 'code', 'geography code', exclude_columns)
    map_html = folium_map._repr_html_()  # Get HTML representation of the folium map

    return render_template('index.html', map_html=map_html)

@app.route('/get_chart_data/<region_id>')
def get_chart_data(region_id):
    # Fetch data for the region, create chart data
    # This should ideally fetch data from your database or data source
    chart_data = {
        'labels': ['Data Point 1', 'Data Point 2'],
        'values': [100, 200],
        'backgroundColor': ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)'],
        'borderColor': ['rgba(255,99,132,1)', 'rgba(54, 162, 235, 1)']
    }
    return jsonify(chart_data)

@app.route('/download_chart/<region_id>')
def download_chart(region_id):
    # Here you would generate data based on the region_id
    # For demonstration, let's create a simple plot with dummy data
    plt.figure()
    plt.plot([1, 2, 3], [4, 5, 6])  # Example data
    plt.title(f'Statistics for {region_id}')
    
    # Save plot to a bytes buffer instead of file
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Send buffer as a file
    return send_file(buf, as_attachment=True, mimetype='image/png', attachment_filename=f'{region_id}_chart.png')

if __name__ == '__main__':
    app.run(debug=True)
