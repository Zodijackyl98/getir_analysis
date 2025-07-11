
import pandas as pd
from sklearn.cluster import KMeans
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt




df = pd.read_csv(r"C:\Python_Works\py\getir\csv\sip_war_with_routes.csv", sep=',')

df = df.dropna(subset=['route_mid_lon', 'route_mid_lat'])

# clustering icin koordinatlarin hazırlanması
midpoints = df[['route_mid_lon', 'route_mid_lat']].values


k = 4  # istenilen servis noktalarının sayısı
kmeans = KMeans(n_clusters=k, random_state=42).fit(midpoints)

# Step 5: Add cluster labels to dataframe
df['service_cluster'] = kmeans.labels_

# servis noktalarının geodataframe'i oluşturulur
service_points = pd.DataFrame(kmeans.cluster_centers_, columns=['longitude_sp', 'latitude_sp'])
service_points['service_point_id'] = [f'sp_{i+1}' for i in range(k)]
gdf_service_points = gpd.GeoDataFrame(
    service_points,
    geometry=[Point(xy) for xy in zip(service_points['longitude_sp'], service_points['latitude_sp'])],
    crs="EPSG:4326"
)

# tamemen opsiyonel
df.to_csv(r"C:\Python_Works\py\getir\csv\sip_war_with_clusters.csv", index=False) 

# zorunlu
gdf_service_points.to_file(r"C:\Python_Works\py\getir\qgis_related\service_points.geojson", driver='GeoJSON')

# optimum servis noktasının belirlenmesi için yardımcı grafik
inertias = []
k_values = list(range(2, 10))  # You can expand the range if needed

for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(midpoints)
    inertias.append(kmeans.inertia_)

# Plot the inertia vs. k
plt.figure(figsize=(8, 5))
plt.plot(k_values, inertias, marker='o', linestyle='-')
plt.title('Elbow Method: Inertia vs. Number of Service Points (k)')
plt.xlabel('Number of Service Points (k)')
plt.ylabel('Inertia (Sum of Squared Distances)')
plt.grid(True)
plt.xticks(k_values)
plt.tight_layout()