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

# Make sure columns are lowercase
df_warehouse.columns = [col.lower() for col in df_warehouse.columns]

# STEP 2 — Aggregate delivery stats by nearest warehouse
df_duration_stats = df_siparis.groupby('nearest_warehouse').agg(
    min_duration=('delivery_duration', 'min'),
    max_duration=('delivery_duration', 'max'),
    avg_duration=('delivery_duration', 'mean'),
    median_duration=('delivery_duration', 'median')
).reset_index()

# Optional: population stddev
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

# STEP 4 — Convert HALF of median delivery time to seconds
df_merged['half_median_sec'] = (df_merged['median_duration'] * 30).astype(int)

# STEP 5 — Create isochrones from ORS
client = openrouteservice.Client(key=api_key)  # Replace with your actual API key

isochrones = []

for idx, row in df_merged.iterrows():
    coords = [row['longitude'], row['latitude']]
    try:
        response = client.isochrones(
            locations=[coords],
            profile='driving-car',
            range=[row['half_median_sec']],
            units='m',
            interval=None,
            location_type='start'
        )
        polygon = shape(response['features'][0]['geometry'])
        isochrones.append({
            'warehouse_num': row['warehouse_num'],
            'half_median_min': row['median_duration'] / 2,
            'geometry': polygon
        })
    except Exception as e:
        print(f"Failed for warehouse {row['warehouse_num']}: {e}")

# STEP 6 — Export to GeoJSON
gdf_isochrones = gpd.GeoDataFrame(isochrones, crs='EPSG:4326')
gdf_isochrones.to_file("C:/Python_Works/py/getir/qgis_related/warehouse_isochrones_half_median.geojson", driver='GeoJSON')
