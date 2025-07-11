-- Assuming you already have geometry columns for orders and warehouses


-- Her sipariş için en yakın warehouselerin atanması
SELECT
  s.order_id,
  w.warehouse_num AS nearest_warehouse,
  ST_Distance(s.geom::geography, w.geom::geography) AS distance_m
FROM
  siparis s
JOIN LATERAL (
  SELECT warehouse_num, geom
  FROM warehouse
  ORDER BY s.geom <-> geom  -- spatial index kullanımı
  LIMIT 1
) w ON TRUE;

ALTER TABLE siparis ADD COLUMN nearest_warehouse TEXT;

-- siparişlerin en yakın warehouselere göre güncellenmesi
UPDATE siparis s
SET
  nearest_warehouse = w.nearest_warehouse,
  distance_to_warehouse = w.distance_m
FROM (
  SELECT
    s.fid,
    w.warehouse_num AS nearest_warehouse,
    ST_Distance(s.geom::geography, w.geom::geography) AS distance_m
  FROM siparis s
  JOIN LATERAL (
    SELECT warehouse_num, geom
    FROM warehouse
    ORDER BY s.geom <-> geom
    LIMIT 1
  ) w ON TRUE
) AS w
WHERE s.fid = w.fid;

-- /getir/python_related/getir_data.py çıktısı olan bursa_district.geojson dosyası QGIS

ALTER TABLE siparis ADD COLUMN district_name TEXT;

UPDATE siparis s
SET district_name = d.name 
FROM bursa_district d
WHERE ST_Within(s.geom, d.geom);

ALTER TABLE warehouse ADD COLUMN district_name TEXT;

UPDATE warehouse w
SET district_name = d.name 
FROM bursa_district d
WHERE ST_Within(w.geom, d.geom);

-- /getir/qgis_related/bursa_mahalle_valid.geojson dosyasının, postgreSQL database içerisine geom verileri 
-- oluşturularak aktarılması sonrası aşağıda aşamaara devam edilir.

ALTER TABLE siparis ADD COLUMN hood_name TEXT;

UPDATE siparis s
SET hood_name = d.name 
FROM bursa_mahalle_valid d
WHERE ST_Within(s.geom, d.geom);

ALTER TABLE warehouse ADD COLUMN hood_name TEXT;

UPDATE warehouse w
SET hood_name = d.name 
FROM bursa_mahalle_valid d
WHERE ST_Within(w.geom, d.geom);

-- bursa mahallelerine ait oldukları belediyelerin ataması yapılır

ALTER TABLE bursa_mahalle_valid ADD COLUMN district_name TEXT;

UPDATE bursa_mahalle_valid b
SET district_name = d.name
FROM bursa_district d
WHERE ST_Within(b.geom, d.geom);

-- (opsiyonel) within uygulanmasına rağmen null kalan değerleri Intersects ile tamamlama
UPDATE bursa_mahalle_valid b
SET district_name = d.name
FROM bursa_district d
WHERE b.district_name IS NULL
  AND ST_Intersects(b.geom, d.geom);



-- mahalle bazlı nüfus yoğunluğu için önce alan hesabı sonra yoğunluk hesabı
-- bursa_mahalle_valid ve mah_pop_mathched üretilmeden çalışmaz

ALTER TABLE bursa_mahalle_valid ADD COLUMN area_km2 NUMERIC;

UPDATE bursa_mahalle_valid
SET area_km2 = ROUND((ST_Area(geom::geography) / 1000000)::NUMERIC, 4);

CREATE TABLE mah_pop_density AS
SELECT 
  b.name AS hood_name,
  b.district_name,
  b.geom,
  b.area_km2,
  m.population,
  ROUND(m.population::NUMERIC / NULLIF(b.area_km2, 0), 2) AS pop_density
FROM bursa_mahalle_valid b
JOIN mahalle_pop_matched m
  ON b.name = m.hood_name AND b.district_name = m.district_name;

-- Bursa_mahalle_valid'e yüz ölçümü ataması yapılmadan çalışmaz.
-- Sipariş yoğunluğunun hesaplanması ve tabloya dönüştürülmesi
CREATE TABLE sip_density_per_hood AS 
SELECT 
  b.name AS hood_name,
  b.district_name,
  b.geom,
  b.area_km2,
  pop.population,
  orders.sip_count,
  ROUND(pop.population / NULLIF(b.area_km2, 0), 2) AS population_density,
  ROUND(orders.sip_count::NUMERIC / NULLIF(b.area_km2, 0), 2) AS order_density
FROM bursa_mahalle_valid b
JOIN mahalle_pop_matched pop 
  ON b.name = pop.hood_name AND b.district_name = pop.district_name
JOIN order_counts_by_hood orders 
  ON b.name = orders.hood_name AND b.district_name = orders.district_name;







