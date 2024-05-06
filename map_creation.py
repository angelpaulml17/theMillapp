import folium
from folium import GeoJson
import geopandas as gpd
import pandas as pd
from folium import GeoJson, Map
from folium.features import GeoJsonTooltip
import geopandas as gpd
import pandas as pd
import folium
from folium.features import GeoJsonTooltip
import json
import mapclassify as mc
from branca.colormap import linear
from branca.colormap import LinearColormap
def get_data_for_region(level, LevelPath,code, region_id, exclude_columns):
    """Fetch and return data for a specific region, excluding specified columns."""
    gdf = gpd.read_file(LevelPath)
    csv_data = pd.read_csv(level)
    csv_data['geography code'] = csv_data['geography code'].astype(str)
    gdf[code] = gdf[code].astype(str)
    merged_gdf = gdf.merge(csv_data, left_on=code, right_on='geography code', how='inner')
    print(merged_gdf.columns)
    print('inside')
    print(region_id)
    try:
        # Assuming `region_id` is a unique identifier in the DataFrame
        region_data = merged_gdf[merged_gdf['geography code'] == region_id]
        # Exclude specified columns and return the first match
        tooltip_data = region_data[[col for col in csv_data.columns if col not in exclude_columns]].iloc[0]
        #print(tooltip_data.columns)
        return tooltip_data.to_dict()
    except IndexError:
        # Handle cases where no data is found for the region_id
        print(f"No data found for region ID {region_id}")
        return None
    
def add_clickable_markers(map_folium, gdf, unique_id_column):
    # Add custom JavaScript for handling clicks
    script = f"""
    <script>


document.addEventListener("DOMContentLoaded", function() {{
    // Since tooltips are dynamically created, we need to listen to mouseover events
    // to have a chance to intercept them when they appear.
    document.addEventListener('click', function(event) {{
        // This function tries to find the tooltip from the event target.
        var tooltipElement = findTooltip(event.target);
        var tooltips = document.querySelectorAll('.leaflet-tooltip');
        console.log('tooltips')
        if (tooltips.length) {{
                        // Assuming the last tooltip in the DOM is the one you're hovering over
                        var lastTooltip = tooltips[tooltips.length - 1];
                        console.log(lastTooltip)
                        // Extract the geography code from the tooltip content
                        // This assumes the tooltip's inner text starts with "Geography Code: "
                        if (lastTooltip) {{
          // Extract the text content from the first <td> element of the tooltip
          const geographyCode = lastTooltip.querySelector('table tr td').textContent;
          
          // Log the geography code for debugging
          console.log('Geography Code:', geographyCode);
          if (geographyCode) {{
                fetch(`/download_chart/${{geographyCode}}`)
                    .then(response => response.json())
                    .then(data => {{
                        console.log(data.img_data);
                        console.log(parent.document.getElementById('chart-container'));
                        if (data.img_data) {{
                            parent.document.getElementById('chart-container').innerHTML = `<img src="${{data.img_data}}" style="width:100%; height:100%;">`;
                            parent.document.getElementById('chart-container').innerHTML += `<button onclick="downloadImage('${{data.img_data}}', '${{geographyCode}}.png')">Download Chart</button>`;
                        }} else {{
                            parent.document.getElementById('chart-container').innerHTML = 'No chart available.';
                        }}
                    }})
                    .catch(error => console.error('Error fetching chart:', error));
            }}
          
        }} else {{
          console.error('Tooltip not found.');
        }}
                    }}
    }});
}});

// Helper function to find the tooltip from the event target
function findTooltip(target) {{
    // Check if the target or its parents have a class that is used by Leaflet tooltips
    while (target) {{
        if (target.classList && target.classList.contains('leaflet-tooltip-pane')) {{
            return target;
        }}
        target = target.parentNode;
    }}
    return null; // Tooltip not found
}}
    </script>
    """
    map_folium.get_root().html.add_child(folium.Element(script))
# Define a function to create a legend with your colors
def generate_legend(colors, value_min, value_max):
    step = (value_max - value_min) / len(colors)
    legend_html = '<div style="position: fixed; bottom: 10px; left: 10px; width: 150px; background-color: white; border:1px solid grey; z-index:9999;">'
    legend_html += '<h4>Legend</h4>'
    for i, color in enumerate(colors):
        legend_html += '<i style="background: {}; width: 20px; height: 20px; display: inline-block;"></i> '.format(color)
        legend_html += '{:.2f} - {:.2f}<br>'.format(value_min + i * step, value_min + (i + 1) * step)
    legend_html += '</div>'
    return legend_html
def create_interactive_map(shapefile_path, data_csv_path, merge_on_shapefile, merge_on_csv,  exclude_columns=None):
    # Load and prepare data
    gdf = gpd.read_file(shapefile_path)
    print(gdf)
    csv_data = pd.read_csv(data_csv_path)
    csv_data[merge_on_csv] = csv_data[merge_on_csv].astype(str)
    gdf[merge_on_shapefile] = gdf[merge_on_shapefile].astype(str)
    merged_gdf = gdf.merge(csv_data, left_on=merge_on_shapefile, right_on=merge_on_csv, how='inner')
    # Compute the average of columns from the 4th to the end
    data_for_classification = csv_data.iloc[:, 3:].mean(axis=1)

    # Add this average data back to the merged GeoDataFrame
    merged_gdf['avg_value'] = data_for_classification

    # Classify the data based on the average values
    classifier = mc.Quantiles(merged_gdf['avg_value'], k=5)
    merged_gdf['category'] = classifier.yb  # Adds the bin/category to the dataframe

    # Get min and max of the average values for the legend
    value_min = merged_gdf['avg_value'].min()
    value_max = merged_gdf['avg_value'].max()

    # Define color scheme for 5 bins
    colors = ['#fec5af', '#f4979a', '#eb6885', '#e33970', '#db0a5b']
    color_scale = folium.LinearColormap(colors, vmin=0, vmax=4)
    merged_gdf['color'] = merged_gdf['category'].apply(lambda x: color_scale(x))


        # Add legend to map
    legend_html = generate_legend(colors, value_min, value_max)
    
    if 'geometry' in merged_gdf.columns:
        merged_gdf = merged_gdf.to_crs(epsg=4326)
        geojson_data = json.loads(merged_gdf.to_json())
        print(geojson_data['features'][0])
        # Create a Folium map at a suitable location and zoom level
        center = [merged_gdf.geometry.centroid.y.mean(), merged_gdf.geometry.centroid.x.mean()]
        map_folium = folium.Map(location=center, zoom_start=10, tiles='cartodbpositron')
        if exclude_columns:
            tooltip_fields = [col for col in csv_data.columns if col not in exclude_columns]
            print(tooltip_fields)
        else:
            tooltip_fields = list(csv_data.columns)
        tooltip_fields.append('avg_value')

        # Add GeoJson layer
        folium.GeoJson(
            geojson_data,
            style_function=lambda x: {'fillColor': merged_gdf.loc[merged_gdf['geography code'] == x['properties']['geography code'], 'color'].values[0],
                                      'color': 'black', 'weight': 0.1, 'fillOpacity': 0.7},
            tooltip=folium.features.GeoJsonTooltip(fields=tooltip_fields)
        ).add_to(map_folium)
        # Define your custom color scale
        
        # map_folium.add_child(color_scale)
        map_folium.get_root().html.add_child(folium.Element(legend_html))
        # Add clickable markers
        add_clickable_markers(map_folium, merged_gdf, 'id')
        
        

        map_folium.save('templates/map.html')
        return map_folium
    else:
        print("Failed to find geometry data in merged DataFrame.")

