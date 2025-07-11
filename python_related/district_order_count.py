import geopandas as gpd
from sqlalchemy import create_engine

engine = create_engine("postgresql://mert:password@localhost:5432/getir")

query = """
SELECT 
  d.name AS district_name,
  COUNT(s.fid) AS sip_count,
  d.geom
FROM bursa_district d
LEFT JOIN siparis s
  ON ST_Within(s.geom, d.geom)
GROUP BY d.name, d.geom
HAVING COUNT(s.fid) != 0
ORDER BY sip_count DESC;
     """

gdf = gpd.read_postgis(query, engine, geom_col="geom")
gdf.to_file("C:/Python_Works/py/getir/qgis_related/district_order_count.geojson", driver="GeoJSON")

