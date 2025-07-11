-- ===============================================
-- ✅ Add Columns if Not Exist
-- ===============================================
ALTER TABLE siparis ADD COLUMN IF NOT EXISTS district_name TEXT;
ALTER TABLE siparis ADD COLUMN IF NOT EXISTS hood_name TEXT;
ALTER TABLE siparis ADD COLUMN IF NOT EXISTS nearest_warehouse TEXT;
ALTER TABLE siparis ADD COLUMN IF NOT EXISTS distance_to_warehouse DOUBLE PRECISION;

ALTER TABLE warehouse ADD COLUMN IF NOT EXISTS district_name TEXT;
ALTER TABLE warehouse ADD COLUMN IF NOT EXISTS hood_name TEXT;

ALTER TABLE bursa_mahalle_valid ADD COLUMN IF NOT EXISTS district_name TEXT;

-- ===============================================
-- ✅ Reset Columns Before Update (Optional Clean)
-- ===============================================
UPDATE siparis SET district_name = NULL, hood_name = NULL, nearest_warehouse = NULL, distance_to_warehouse = NULL;
UPDATE warehouse SET district_name = NULL, hood_name = NULL;
UPDATE bursa_mahalle_valid SET district_name = NULL;

-- ===============================================
-- ✅ Assign Districts to Mahalle (Strict then Fallback)
-- ===============================================
-- Step 1: ST_Within
UPDATE bursa_mahalle_valid b
SET district_name = d."shapeName"
FROM districts d
WHERE ST_Within(b.geom, d.geom);

-- Step 2: ST_Intersects fallback
UPDATE bursa_mahalle_valid b
SET district_name = d."shapeName"
FROM districts d
WHERE b.district_name IS NULL AND ST_Intersects(b.geom, d.geom);

-- ===============================================
-- ✅ Assign Districts to siparis
-- ===============================================
UPDATE siparis s
SET district_name = d."shapeName"
FROM districts d
WHERE ST_Within(s.geom, d.geom);

UPDATE siparis s
SET district_name = d."shapeName"
FROM districts d
WHERE s.district_name IS NULL AND ST_Intersects(s.geom, d.geom);

-- ===============================================
-- ✅ Assign Districts to warehouse
-- ===============================================
UPDATE warehouse w
SET district_name = d."shapeName"
FROM districts d
WHERE ST_Within(w.geom, d.geom);

UPDATE warehouse w
SET district_name = d."shapeName"
FROM districts d
WHERE w.district_name IS NULL AND ST_Intersects(w.geom, d.geom);

-- ===============================================
-- ✅ Assign Hood Names to siparis
-- ===============================================
UPDATE siparis s
SET hood_name = b.name
FROM bursa_mahalle_valid b
WHERE ST_Within(s.geom, b.geom);

UPDATE siparis s
SET hood_name = b.name
FROM bursa_mahalle_valid b
WHERE s.hood_name IS NULL AND ST_Intersects(s.geom, b.geom);

-- ===============================================
-- ✅ Assign Hood Names to warehouse
-- ===============================================
UPDATE warehouse w
SET hood_name = b.name
FROM bursa_mahalle_valid b
WHERE ST_Within(w.geom, b.geom);

UPDATE warehouse w
SET hood_name = b.name
FROM bursa_mahalle_valid b
WHERE w.hood_name IS NULL AND ST_Intersects(w.geom, b.geom);

-- ===============================================
-- ✅ Calculate Nearest Warehouse per siparis
-- ===============================================
-- Assumes 'fid' is a unique identifier in siparis table
UPDATE siparis s
SET nearest_warehouse = sub.nearest_warehouse,
    distance_to_warehouse = sub.distance_m
FROM (
  SELECT s.fid,
         w.warehouse_num AS nearest_warehouse,
         ST_Distance(s.geom::geography, w.geom::geography) AS distance_m
  FROM siparis s
  JOIN LATERAL (
    SELECT warehouse_num, geom
    FROM warehouse
    ORDER BY s.geom <-> geom
    LIMIT 1
  ) w ON TRUE
) sub
WHERE s.fid = sub.fid;

-- ===============================================
-- ✅ Manual Fix for Görükle
-- ===============================================
UPDATE bursa_mahalle_valid
SET district_name = 'Nilüfer'
WHERE name = 'Görükle Mahallesi' AND district_name != 'Nilüfer';
