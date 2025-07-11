
import openrouteservice
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString
from sqlalchemy import create_engine

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("ORS_API_KEY")


# Connect to ORS
client = openrouteservice.Client(key=api_key)

df_siparis = pd.read_csv(r"C:\Python_Works\py\getir\csv\siparis_w_geom.csv", sep = ',')
df_warehouse = pd.read_csv(r"C:\Python_Works\py\getir\csv\warehouse_w_geom.csv", sep = ',')

# warehouse tablosundaki büyük harf ile başlayan "Longitude" ve "Latitude" problemi için sıfırdan veritabanı oluşturuluyorsa konum adının
# ALTER TABLE warehouse RENAME COLUMN "Longitude" TO longitude; 
# ALTER TABLE warehouse RENAME COLUMN "Latitude" TO latitude;    şekillerinde postgreSQL'den değiştirilmesi tavsiye edilir.

war_geo_col_fix = []
for i in df_warehouse.columns:
    war_geo_col_fix.append(i.lower())
    
df_warehouse.columns = war_geo_col_fix    

# Example warehouse coordinate: [lon, lat]
war_geo_tup = [(i[0],i[1]) for i in df_warehouse[['longitude','latitude']].values]
coords = [war_geo_tup[0][0], war_geo_tup[0][1]]

# en yakın warehouselere göre sınıflandırılmış konum bilgileri, ortalamaları alınmak koşuluyla
df_sip_ser_lon = df_siparis[['nearest_warehouse','longitude']].groupby('nearest_warehouse').agg(['mean'])
df_sip_ser_lat = df_siparis[['nearest_warehouse','latitude']].groupby('nearest_warehouse').agg(['mean'])
df_sip_ser_fin = pd.concat([df_sip_ser_lon,df_sip_ser_lat], axis = 1)

df_war_ser_lon = df_warehouse[['warehouse_num','longitude']].groupby('warehouse_num').agg(['mean'])
df_war_ser_lat = df_warehouse[['warehouse_num','latitude']].groupby('warehouse_num').agg(['mean'])
df_war_ser_fin = pd.concat([df_war_ser_lon,df_war_ser_lat], axis = 1)


df_sip_ser_fin_cols = []
for i in df_sip_ser_fin.columns:
    df_sip_ser_fin_cols.append(i[0] + '_s')
    
df_sip_ser_fin.columns = df_sip_ser_fin_cols

df_war_ser_fin_cols = []
for i in df_war_ser_fin.columns:
    df_war_ser_fin_cols.append(i[0] + '_w')
    
df_war_ser_fin.columns = df_war_ser_fin_cols    

df_ser_fin = pd.concat([df_sip_ser_fin, df_war_ser_fin], axis = 1)

df_sip_ser_fin.to_csv(r"C:\Python_Works\py\getir\csv\siparis_ser.csv", index = True, sep = ',')
df_war_ser_fin.to_csv(r"C:\Python_Works\py\getir\csv\warehouse_ser.csv", index = True, sep = ',')
df_ser_fin.to_csv(r"C:\Python_Works\py\getir\csv\sip_war_combined_ser.csv", index = True, sep = ',')


def calculate_route_with_midpoint(row):
    try:
        start = [row['longitude_w'], row['latitude_w']]
        end = [row['longitude_s'], row['latitude_s']]

        route = client.directions(
            coordinates=[start, end],
            profile='cycling-regular',
            format='geojson'
        )

        summary = route['features'][0]['properties']['summary']
        distance_km = summary['distance'] / 1000
        duration_min = summary['duration'] / 60
        geometry = route['features'][0]['geometry']

        # Get coordinates from route line and find the midpoint
        coords = geometry['coordinates']
        if coords and len(coords) > 0:
            mid_index = len(coords) // 2
            route_mid_lon, route_mid_lat = coords[mid_index]
        else:
            route_mid_lon, route_mid_lat = None, None

        return pd.Series([distance_km, duration_min, geometry, route_mid_lon, route_mid_lat])

    except Exception as e:
        print(f"Error for {row.name}: {e}")
        return pd.Series([None, None, None, None, None])

# Apply the function to each warehouse
df_ser_fin[['route_km', 'route_min', 'route_geometry', 'route_mid_lon', 'route_mid_lat']] = (
    df_ser_fin.apply(calculate_route_with_midpoint, axis=1)
)

# Convert ORS GeoJSON-style coordinate lists into shapely LineStrings
df_ser_fin['route_line'] = df_ser_fin['route_geometry'].apply(
    lambda geom: LineString(geom['coordinates']) if geom else None
)

gdf_routes = gpd.GeoDataFrame(df_ser_fin, geometry='route_line', crs='EPSG:4326')

gdf_routes.to_file(r"C:\Python_Works\py\getir\qgis_related\routes_bicycle.geojson", driver="GeoJSON")
df_ser_fin.to_csv(r"C:\Python_Works\py\getir\csv\sip_war_with_routes_bicycle.csv", index=True, sep=',') #Rota oluşturmak için kullanılacak


db_user = 'mert'
db_pass = 'password'
db_host = 'localhost'
db_port = '5432'
db_name = 'getir'


engine = create_engine(f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}')


df_ser_fin.drop(columns=['route_geometry'], inplace=True)

df_ser_fin['route_line'] = df_ser_fin['route_line'].apply(
    lambda x: x.wkt if x else None
)

# agırlıklı siparis noktası, warehouse nokları ve güzergahlar üzerindeki orta noktaları barındırıyor
df_ser_fin.to_sql("sip_war_with_routes_bicycle", con=engine, if_exists='replace', index=True)

# agırlıklı siparis noktaları
df_sip_ser_fin.to_sql("siparis_ser_bicycle", con=engine, if_exists='replace', index=True)


# ikinci kez çalıştırılırsa uyarı verir, problem yaratmaz.
query = """
    ALTER TABLE siparis_ser_bicycle ADD COLUMN siparis_point geometry(Point, 4326);
    ALTER TABLE sip_war_with_routes_bicycle ADD COLUMN midpoint geometry(Point, 4326);


    UPDATE siparis_ser_bicycle SET siparis_point = ST_SetSRID(ST_MakePoint(longitude_s, latitude_s), 4326);
    UPDATE sip_war_with_routes_bicycle SET midpoint = ST_SetSRID(ST_MakePoint(route_mid_lon, route_mid_lat), 4326);
        """
        
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(text(query))
    conn.commit()




