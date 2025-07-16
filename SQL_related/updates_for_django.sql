-- CREATE VIEW sip_per_district AS SELECT s.district_name, count(*) FROM siparis s GROUP BY s.district_name;

-- CREATE VIEW sip_duration_stats AS SELECT 
--   nearest_warehouse,
--   MIN(delivery_duration) AS min_duration,
--   MAX(delivery_duration) AS max_duration,
--   AVG(delivery_duration) AS avg_duration,
--   STDDEV_POP(delivery_duration) AS std_dev_pop,
--   PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY delivery_duration) AS median_duration
-- FROM siparis
-- GROUP BY nearest_warehouse;

-- CREATE VIEW sip_per_capita AS
-- SELECT 
--   o.district_name,
--   o.hood_name,
--   m.population,
--   o.sip_count,
--   ROUND(o.sip_count::numeric / NULLIF(m.population, 0), 4) AS sip_per_capita
-- FROM order_counts_by_hood o
-- JOIN mahalle_pop_matched m 
--   ON o.district_name = m.district_name
--  AND o.hood_name = m.hood_name
-- WHERE ST_Within(m.geom, o.geom) ORDER BY sip_per_capita;

-- CREATE VIEW pop_density_per_hood AS SELECT 
--   b.name AS hood_name,
--   b.district_name,
--   b.area_km2,
--   m.population,
--   ROUND(m.population::NUMERIC / NULLIF(b.area_km2, 0), 2) AS pop_density
-- FROM bursa_mahalle_valid b
-- JOIN mahalle_pop_matched m
--   ON b.name = m.hood_name AND b.district_name = m.district_name 
--   ORDER BY pop_density DESC LIMIT 10;

-- CREATE VIEW sip_density AS SELECT 
--   b.name AS hood_name,
--   b.district_name,
--   b.area_km2,
--   pop.population,
--   orders.sip_count,
--   ROUND(pop.population / NULLIF(b.area_km2, 0), 2) AS population_density,
--   ROUND(orders.sip_count::NUMERIC / NULLIF(b.area_km2, 0), 2) AS order_density
-- FROM bursa_mahalle_valid b
-- JOIN mahalle_pop_matched pop 
--   ON b.name = pop.hood_name AND b.district_name = pop.district_name
-- JOIN order_counts_by_hood orders 
--   ON b.name = orders.hood_name AND b.district_name = orders.district_name
--   ORDER BY order_density DESC;

ALTER TABLE siparis ADD COLUMN id smallserial PRIMARY KEY;
ALTER TABLE sip_per_capita ADD COLUMN id smallserial PRIMARY KEY;
ALTER TABLE sip_density_per_hood ADD COLUMN id smallserial PRIMARY KEY;
