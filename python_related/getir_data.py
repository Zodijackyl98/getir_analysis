# -*- coding: utf-8 -*-
"""
Created on Tue Jul  8 17:51:52 2025

@author: merts
"""

import pandas as pd
import math 
import geopandas as gpd
from shapely.geometry import MultiPolygon, Polygon

# PostgreSQL'de geom sütunları oluşturulduktan sonra import edilmeli
df_siparis = pd.read_csv(r"C:\Python_Works\py\getir\csv\siparis_w_geom.csv", sep = ',')
df_warehouse = pd.read_csv(r"C:\Python_Works\py\getir\csv\warehouse_w_geom.csv", sep = ',')

war_geo_col_fix = []
for i in df_warehouse.columns:
    war_geo_col_fix.append(i.lower())

df_warehouse.columns = war_geo_col_fix


# İhtiyaç olursa diye iki nokta arası mesafeyi haversine formulu ile hesaplayan fonksiyon
def haversine(coord1, coord2):
    # Coordinates in decimal degrees (e.g. 2.89078, 12.79797)
    lon1, lat1 = coord1
    lon2, lat2 = coord2
    R = 6371000  # radius of Earth in meters
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)
    
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    meters = R * c  # output distance in meters
    km = meters / 1000.0  # output distance in kilometers
    
    meters = round(meters)
    km = round(km, 3)
    # print(f"Distance: {meters} m")
    # print(f"Distance: {km} km")

    return meters

sip_geo_tup = [(i[0],i[1]) for i in df_siparis[['longitude','latitude']].values]
war_geo_tup = [(i[0],i[1]) for i in df_warehouse[['longitude','latitude']].values]

dist_ex = haversine(coord1 = sip_geo_tup[0], coord2 = war_geo_tup[0])

print(dist_ex)


# Load GeoJSON, multypolygona dönüştürmek gerekli
gdf = gpd.read_file(r"C:\Python_Works\py\getir\qgis_related\bursa_district.geojson", encoding='utf-8')

# Convert all Polygons to MultiPolygons
def ensure_multipolygon(geom):
    if isinstance(geom, Polygon):
        return MultiPolygon([geom])
    return geom

gdf["geometry"] = gdf["geometry"].apply(ensure_multipolygon)


# Save back to GeoJSON (make sure to use UTF-8)
gdf.to_file(r"C:\Python_Works\py\getir\qgis_related\bursa_district.geojson", driver="GeoJSON", encoding="utf-8")


