import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import shape
import openrouteservice

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("ORS_API_KEY")


# STEP 1 — Load siparis and warehouse CSVs
df_siparis = pd.read_csv("C:/Python_Works/py/getir/csv/siparis_w_geom.csv")
df_warehouse = pd.read_csv("C:/Python_Works/py/getir/csv/warehouse_w_geom.csv")

# Lowercase column names for consistency
df_warehouse.columns = [col.lower() for col in df_warehouse.columns]

# STEP 2 — Aggregate delivery stats by nearest warehouse
df_duration_stats = df_siparis.groupby('nearest_warehouse').agg(
    min_duration=('delivery_duration', 'min'),
    max_duration=('delivery_duration', 'max'),
    avg_duration=('delivery_duration', 'mean'),
    median_duration=('delivery_duration', 'median')
).reset_index()

# Optional: calculate population stddev
df_duration_stats['std_dev_pop'] = (
    df_siparis.groupby('nearest_warehouse')['delivery_duration']
    .apply(lambda x: np.std(x, ddof=0))
    .values
)

# STEP 3 — Merge delivery stats with warehouse coordinates
df_merged = pd.merge(
    df_duration_stats,
    df_warehouse,
    left_on='nearest_warehouse',
    right_on='warehouse_num',
    how='inner'
)

# STEP 4 — Convert min delivery time to seconds
df_merged['min_sec'] = (df_merged['min_duration'] * 60).astype(int)

# STEP 5 — Generate isochrones using ORS
client = openrouteservice.Client(key=api_key)

isochrones = []

for idx, row in df_merged.iterrows():
    coords = [row['longitude'], row['latitude']]
    try:
        response = client.isochrones(
            locations=[coords],
            profile='driving-car',
            range=[row['min_sec']],
            units='m',
            interval=None,
            location_type='start'
        )
        polygon = shape(response['features'][0]['geometry'])
        isochrones.append({
            'warehouse_num': row['warehouse_num'],
            'min_duration_min': row['min_duration'],
            'geometry': polygon
        })
    except Exception as e:
        print(f"Failed for warehouse {row['warehouse_num']}: {e}")

# STEP 6 — Convert to GeoDataFrame and export
gdf_isochrones = gpd.GeoDataFrame(isochrones, geometry='geometry', crs='EPSG:4326')

# Save to GeoJSON for QGIS
gdf_isochrones.to_file("C:/Python_Works/py/getir/qgis_related/warehouse_isochrones_min.geojson", driver='GeoJSON')

print("saved successfully.")
