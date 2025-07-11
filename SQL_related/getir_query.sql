SELECT * FROM siparis ORDER BY nearest_warehouse, delivery_duration;

-- en yakin depoya göre ortalama mesafe
SELECT nearest_warehouse, avg(distance_to_warehouse) FROM siparis GROUP BY nearest_warehouse ORDER BY nearest_warehouse ASC;

-- en yakın depoya göre ortalamamın üzerinde teslimat süresi
SELECT s.*
FROM siparis s
JOIN (
  SELECT nearest_warehouse, AVG(distance_to_warehouse) AS avg_dist
  FROM siparis
  GROUP BY nearest_warehouse
) f ON s.nearest_warehouse = f.nearest_warehouse
WHERE s.distance_to_warehouse > f.avg_dist AND s.nearest_warehouse = 'wh_1';


-- Order count with respected to nearist warehouse
SELECT nearest_warehouse, count(*) FROM siparis GROUP BY nearest_warehouse;


-- Depoların bulunduğu ilçeler
SELECT
  district_name,
  warehouse_num,
  hood_name
FROM warehouse
ORDER BY district_name, warehouse_num;


-- Belediyelere göre sipariş sayısı
SELECT district_name, count(*) FROM siparis GROUP BY district_name;

-- Belediyelere göre depo sayısı ve bulunduğu mahalleler
SELECT district_name, count(*) FROM warehouse GROUP BY district_name;
SELECT district_name, hood_name, count(*) FROM warehouse GROUP BY district_name, hood_name;

-- Belediyelere göre sipariş sayısı
SELECT s.district_name, count(*) FROM siparis s GROUP BY s.district_name;
SELECT s.district_name, w.warehouse_num, count(*) FROM siparis s JOIN warehouse w ON s.district_name = w.district_name GROUP BY s.district_name, w.warehouse_num;

SELECT 
  b.ilce, 
  b.ilce_nufusu, 
  s.nearest_warehouse, 
  COUNT(s.order_id) AS total_orders,
  w_count.num_warehouses
FROM siparis s
JOIN ilce_bursa_nufusu b 
  ON s.district_name = b.ilce
JOIN warehouse w 
  ON w.district_name = s.district_name
JOIN (
  SELECT district_name, COUNT(*) AS num_warehouses
  FROM warehouse
  GROUP BY district_name
) w_count 
  ON w_count.district_name = b.ilce
GROUP BY 
  b.ilce, 
  b.ilce_nufusu, 
  s.nearest_warehouse, 
  w_count.num_warehouses;

-- siparis suresine göre min,max,ortanca ve ortalama degerleri
SELECT 
  nearest_warehouse,
  MIN(delivery_duration) AS min_duration,
  MAX(delivery_duration) AS max_duration,
  AVG(delivery_duration) AS avg_duration,
  STDDEV_POP(delivery_duration) AS std_dev_pop,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY delivery_duration) AS median_duration
FROM siparis
GROUP BY nearest_warehouse;


-- Her belediyenin toplam yüz ölçümünü hesapla, siparis sayısı ile birlikte göster
SELECT 
  bursa_district.name,  -- or your district column name
  ROUND((SUM(ST_Area(geom::geography)) / 1000000)::NUMERIC, 2) AS area_sq_km,
  f.sip_count,
  n.ilce_nufusu,
  n.nufus_yuzdesi
FROM bursa_district JOIN (SELECT s.district_name, count(*) sip_count FROM siparis s GROUP BY s.district_name) as f ON f.district_name = bursa_district.name 
JOIN (SELECT ilce,ilce_nufusu,nufus_yuzdesi FROM ilce_bursa_nufusu) AS n ON n.ilce = bursa_district.name
WHERE bursa_district.name IN (SELECT DISTINCT w.district_name FROM warehouse w) 
GROUP BY bursa_district.name, f.sip_count, n.ilce_nufusu,n.nufus_yuzdesi
ORDER BY area_sq_km DESC;

-- Mahalle ve ilçe bazlı sipariş sayıları
SELECT
  b.name AS hood_name,
  b.district_name,
  COUNT(*) AS sip_count
FROM bursa_mahalle_valid b
JOIN siparis s
  ON ST_Within(s.geom, b.geom)
GROUP BY b.name, b.district_name
ORDER BY sip_count DESC;

-- siparis + bursa_mahalla_valid
SELECT * FROM siparis s JOIN bursa_mahalle_valid b ON b.name = s.hood_name;

SELECT name, district_name
FROM bursa_mahalle_valid
WHERE name ILIKE '%görükle%';


-- district validity
SELECT s.district_name AS from_order, b.district_name AS spatial_district, COUNT(*)
FROM siparis s
JOIN bursa_mahalle_valid b ON ST_Within(s.geom, b.geom)
GROUP BY s.district_name, b.district_name
ORDER BY COUNT(*) DESC;


-- İlçelere göre sipariş sayıları
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

-- İlçelere göre en fazla satış yapan mahalleler
WITH mahalle_counts AS (
    SELECT 
        s.district_name,
        s.hood_name,
        COUNT(*) AS sip_count
    FROM siparis s
    WHERE s.district_name IS NOT NULL AND s.hood_name IS NOT NULL
    GROUP BY s.district_name, s.hood_name
),

ranked_mahalle AS (
    SELECT *,
           RANK() OVER (PARTITION BY district_name ORDER BY sip_count DESC) AS rank
    FROM mahalle_counts
)

SELECT
    district_name,
    hood_name,
    sip_count
FROM ranked_mahalle
WHERE rank = 1 OR rank = 2 OR rank = 3
ORDER BY sip_count DESC;


-- siparis count / population
SELECT o.district_name,m.district_name, o.hood_name,m.mahalle_name,m.population,o.sip_count FROM order_counts_by_hood o JOIN mahalle_pop_matched m ON o.district_name = m.district_name
AND o.hood_name = m.mahalle_name AND ST_Within(m.geom, o.geom);

-- her ilçenin en kalabalık 3 mahallesi
SELECT *
FROM (
  SELECT 
    district_name,
    hood_name,
    population,
    ROW_NUMBER() OVER (PARTITION BY district_name ORDER BY population DESC) AS rank
  FROM bursa_pop_all
) ranked
WHERE rank <= 3;

-- sip_count / population = sip_per_capita
SELECT 
  o.district_name,
  o.hood_name,
  m.population,
  o.sip_count,
  ROUND(o.sip_count::numeric / NULLIF(m.population, 0), 4) AS sip_per_capita
FROM order_counts_by_hood o
JOIN mahalle_pop_matched m 
  ON o.district_name = m.district_name
 AND o.hood_name = m.hood_name
WHERE ST_Within(m.geom, o.geom) ORDER BY sip_per_capita DESC LIMIT 10;

-- mahalle bazli alan hesabı
SELECT b.name, district_name,area_km2 FROM bursa_mahalle_valid b ORDER BY area_km2 DESC LIMIT 10;

-- pop_density mahallelere göre
SELECT 
  b.name AS hood_name,
  b.district_name,
  b.area_km2,
  m.population,
  ROUND(m.population::NUMERIC / NULLIF(b.area_km2, 0), 2) AS pop_density
FROM bursa_mahalle_valid b
JOIN mahalle_pop_matched m
  ON b.name = m.hood_name AND b.district_name = m.district_name 
  ORDER BY pop_density DESC LIMIT 10;