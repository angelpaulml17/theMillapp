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

gdf = gpd.read_file('Boundaries-20240419T224611Z-001\Boundaries\WM_Boundaries\WM_MSOAs\WM_MSOAs.shp')
csv_data = pd.read_csv('Collective_Census_2021_folder_filtered-20240419T224609Z-001\Collective_Census_2021_folder_filtered\census2021-ts001\census2021-ts001-ltla-filtered.csv')

print(gdf.columns)
print(csv_data.columns)