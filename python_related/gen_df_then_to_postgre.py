
import pandas as pd
from sqlalchemy import create_engine
import geopandas as gpd


# dizinde bulunan ilçeler ve bunları mahallelerini barındıran fakat csv stardartların uymayan csv dosyalarını düzenler

for i in ['osmangazi', 'nilüfer', 'yıldırım']:
    file_path = fr"C:\Python_Works\py\getir\Stats\extra\bursa_{i}.csv"
    
    df_raw = pd.read_csv(file_path, header=None, skiprows=6, encoding='utf-8')
    
    df_raw = df_raw[df_raw[0].str.contains("Mah.", na=False) & df_raw[0].str.contains(i, case=False, na=False)]
    df_split = df_raw[0].str.split("|", expand=True)[[1, 2]]
    df_split.columns = ['raw_label', 'population']
    
    df_split['hood_name'] = df_split['raw_label'].str.extract(r'/([^/]+ Mah\.)')
    df_split = df_split[df_split['hood_name'].notnull()]
    
    # veri içerisinde baş harfi büyük olacak şekilde sınıflandırılmışlar, baş harfi dönüştürme işlemi 
    df_split['district_name'] = i.capitalize()
    df_split['population'] = pd.to_numeric(df_split['population'], errors='coerce').fillna(0).astype(int)
    
    df_clean = df_split[['district_name', 'hood_name', 'population']].reset_index(drop=True)
    df_clean.to_csv(fr"C:\Python_Works\py\getir\csv\bursa_{i}.csv", index=False)
    

engine = create_engine("postgresql://mert:password@localhost:5432/getir")

# List of district CSVs and their table names
districts = {
    "osmangazi": "bursa_osm_pop",
    "nilüfer": "bursa_nil_pop",
    "yıldırım": "bursa_yil_pop"
}

# Her csv üzerinden döngü yardımıyla import işlemi
for district, table_name in districts.items():
    file_path = fr"C:\Python_Works\py\getir\csv\bursa_{district}.csv"
    
    # Read the file (adjust encoding if needed)
    df = pd.read_csv(file_path, encoding='utf-8')
    
    # Write to PostgreSQL
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print(f"Imported: {table_name}")

#bütün tabloları birleştir
tables = ['bursa_osm_pop', 'bursa_nil_pop', 'bursa_yil_pop']
dfs = [pd.read_sql_table(t, engine) for t in tables]

# Concatenate into one
df_all_pop = pd.concat(dfs, ignore_index=True)

# Optional: clean hood_name whitespace or case
df_all_pop['hood_name'] = df_all_pop['hood_name'].str.strip()
df_all_pop['district_name'] = df_all_pop['district_name'].str.strip()

# Write combined table to PostgreSQL
df_all_pop.to_sql('bursa_pop_all', con=engine, if_exists='replace', index=False)


# sorgu, 

query = """
CREATE EXTENSION IF NOT EXISTS pg_trgm;

SELECT 
  b.name AS hood_name,   
  b.district_name,
  b.geom,
  p.population
FROM bursa_mahalle_valid b
JOIN bursa_pop_all p
  ON b.district_name = p.district_name
 AND similarity(b.name, p.hood_name) > 0.4
ORDER BY similarity(b.name, p.hood_name) DESC;
"""

# Read GeoDataFrame from PostGIS
gdf = gpd.read_postgis(query, engine, geom_col="geom")

# Save as GeoJSON
output_path = "C:/Python_Works/py/getir/qgis_related/mahalle_pop_matched.geojson"
gdf.to_file(output_path, driver="GeoJSON")





