
# Opsiyonel, diğer işlemlere herhangi bir katkısı yok

import pandas as pd
from sqlalchemy import create_engine
import geopandas as gpd

# Parameters
db_user = 'mert'
dbuser_password = 'password'
db_host = 'localhost'
db_port = '5432'
db_name = 'getir'

# Create SQLAlchemy engine
engine = create_engine(f'postgresql://{db_user}:{dbuser_password}@{db_host}:{db_port}/{db_name}')

# Define your SQL query
query = """
SELECT 
    s.*, 
    b.geom AS mahalle_geom  -- ← rename one of the geometries
FROM siparis s
JOIN bursa_mahalle_valid b ON b.name = s.hood_name;

"""

# Run the query and fetch results into a DataFrame
with engine.connect() as conn:
    df = pd.read_sql(query, conn)

# Now `df` contains your result
print(df.head())

df.drop(columns=['geom'], inplace = True)  # if needed

gdf = gpd.read_postgis(query, engine, geom_col='mahalle_geom')

gdf.to_file("C:/Python_Works/py/getir/qgis_related/neighbourhood_based.geojson", driver="GeoJSON")


