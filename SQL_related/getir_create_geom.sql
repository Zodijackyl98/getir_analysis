CREATE EXTENSION IF NOT EXISTS postgis;

ALTER TABLE siparis ADD COLUMN geom geometry(Point, 4326);
ALTER TABLE warehouse ADD COLUMN geom geometry(Point, 4326);

UPDATE siparis SET geom = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326);
UPDATE warehouse SET geom = ST_SetSRID(ST_MakePoint("Longitude", "Latitude"), 4326);

CREATE INDEX idx_siparis_geom ON siparis USING GIST(geom);
CREATE INDEX idx_warehouse_geom ON warehouse USING GIST(geom);

ALTER TABLE warehouse RENAME COLUMN "Warehouse1" TO warehouse_num;
-- ALTER TABLE warehouse RENAME COLUMN "Longitude" TO longitude;
-- ALTER TABLE warehouse RENAME COLUMN "Latitude" TO latitude;
ALTER TABLE siparis RENAME COLUMN "delivery duration" TO delivery_duration;

ALTER TABLE siparis ADD COLUMN distance_to_warehouse DOUBLE PRECISION;

COPY siparis TO 'C:\Python_Works\py\getir\csv\siparis_w_geom.csv' WITH CSV HEADER;
COPY warehouse TO 'C:\Python_Works\py\getir\csv\warehouse_w_geom.csv' WITH CSV HEADER;



