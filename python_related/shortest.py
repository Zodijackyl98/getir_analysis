import pandas as pd
import openrouteservice
import folium

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("ORS_API_KEY")

# Your ORS API key here
client = openrouteservice.Client(key=api_key)

df_siparis = pd.read_csv(r"C:\Python_Works\py\getir\csv\siparis_w_geom.csv", sep = ',')
df_warehouse = pd.read_csv(r"C:\Python_Works\py\getir\csv\warehouse_w_geom.csv", sep = ',')

war_geo_col_fix = []
for i in df_warehouse.columns:
    war_geo_col_fix.append(i.lower())
    
df_warehouse.columns = war_geo_col_fix  

sip_geo_tup = [(i[0],i[1]) for i in df_siparis[['longitude','latitude']].values]
war_geo_tup = [(i[0],i[1]) for i in df_warehouse[['longitude','latitude']].values]


start = [29.098166,40.184361]   # Example: warehouse
end = [29.136059, 40.180739]     # Example: order

# Get the route (shortest by road)
route = client.directions(
    coordinates=[start, end],
    profile='driving-car',         # can also use 'cycling-regular', 'foot-walking', etc.
    format='geojson'
)

# Extract route distance and duration
summary = route['features'][0]['properties']['summary']
distance_km = summary['distance'] / 1000  # in kilometers
duration_min = summary['duration'] / 60   # in minutes

print(f"Distance: {distance_km:.2f} km")
print(f"Duration: {duration_min:.2f} min")

# Optional: Visualize on map
# m = folium.Map(location=[(start[1] + end[1]) / 2, (start[0] + end[0]) / 2], zoom_start=12)
# folium.GeoJson(route, name="route").add_to(m)
# folium.Marker(location=start[::-1], tooltip="Start").add_to(m)
# folium.Marker(location=end[::-1], tooltip="End").add_to(m)
# m.save("shortest_route.html")
