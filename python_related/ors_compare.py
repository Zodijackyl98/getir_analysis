import geopandas as gpd

car_routes_path = r"C:/Python_Works/py/getir/qgis_related/routes.geojson"
bike_routes_path = r"C:/Python_Works/py/getir/qgis_related/routes_bicycle.geojson"


gdf_car_routes = gpd.read_file(car_routes_path)
gdf_bike_routes = gpd.read_file(bike_routes_path)


# gdf_car_routes = gdf_car_routes.reset_index()
# gdf_bike_routes = gdf_bike_routes.reset_index()

gdf_compare = gdf_car_routes.merge(
    gdf_bike_routes,
    left_index=True,
    right_index=True,
    suffixes=('_car', '_bike'))


# Difference in time (minutes) and distance (km)
gdf_compare['delta_minutes'] = gdf_compare['route_min_car'] - gdf_compare['route_min_bike']
gdf_compare['delta_km'] = gdf_compare['route_km_car'] - gdf_compare['route_km_bike']

gdf_compare['min_better'] = gdf_compare['delta_minutes'].apply(
    lambda x: 'car' if x < 0 else ('bike' if x > 0 else 'equal'))

gdf_compare['km_better'] = gdf_compare['delta_km'].apply(
    lambda x: 'car' if x < 0 else ('bike' if x > 0 else 'equal'))

# ufak zaman farkiyla arac veya bisiklet farkı varsa belirleyici olsun diye zaman sınırı
gdf_compare['sig_time_saving'] = gdf_compare['delta_minutes'].apply(
    lambda x: True if abs(x) > 2 else False  # 2 min threshold
)

# wh_* numaralarına göre sıfırlandıysa tekrardan index oluşturma
warehouse_labels = [f"wh_{i+1}" for i in range(len(gdf_compare))]

gdf_compare.index = warehouse_labels
gdf_compare.index.name = 'warehouse_num'


#sig_time_savine 
print(gdf_compare[['route_min_car',
                   'route_min_bike', 'delta_minutes',
                   'min_better', 'km_better','sig_time_saving']])

df_compare_csv = gdf_compare.drop(columns=['route_geometry_car', 'route_geometry_bike'])

df_compare_csv.to_csv("C:/Python_Works/py/getir/csv/route_comparison_car_vs_bike.csv", index=True)

# openpyxl modulü gerekli, şuanlık ihtiyacı yok
# df_compare_csv.to_excel(
#     "C:/Python_Works/py/getir/excel_outputs/route_comparison.xlsx",
#     index=True,
#     float_format="%.2f"  # Keeps decimals clean
# )



