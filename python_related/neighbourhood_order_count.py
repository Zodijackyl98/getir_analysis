import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine


# 1. Database connection
engine = create_engine("postgresql://mert:password@localhost:5432/getir")


# 2. SQL: Count orders per mahalle using spatial join
query = """
SELECT
  b.name AS hood_name,
  b.district_name,
  COUNT(*) AS sip_count
FROM bursa_mahalle_valid b
JOIN siparis s
  ON ST_Within(s.geom, b.geom)
GROUP BY b.name, b.district_name
ORDER BY sip_count DESC;
"""

df_counts = pd.read_sql(query, engine)


# 3. Load mahalle geometries from PostGIS

geo_query = """
SELECT name, district_name, geom
FROM bursa_mahalle_valid
"""

gdf_hoods = gpd.read_postgis(geo_query, engine, geom_col="geom")

# sayıları ile mahalle geometrisinin birleştirilmesi
gdf_merged = gdf_hoods.merge(
    df_counts,
    left_on=["name", "district_name"],
    right_on=["hood_name", "district_name"],
    how="left"
)

# Fill mahalle with 0 orders
gdf_merged["sip_count"] = gdf_merged["sip_count"].fillna(0).astype(int)



# mahalleden hiç sipariş gelmediği takdirde null değer atamasını önlemek için
gdf_merged['hood_name'] = gdf_merged['hood_name'].fillna(gdf_merged['name'])
gdf_merged["sip_count"] = gdf_merged["sip_count"].fillna(0).astype(int)


output_path = "C:/Python_Works/py/getir/qgis_related/order_counts_by_hood.geojson"

gdf_merged.to_file(output_path, driver="GeoJSON")

print(f"GeoJSON saved to:\n{output_path}")


