-- Create Table Script
CREATE TABLE bursa_osmangazi_edu (
    education_level_id SERIAL PRIMARY KEY,
    education_level VARCHAR(50) NOT NULL,
    population_count INT NOT NULL
);

-- Insert Data Script
INSERT INTO bursa_osmangazi_edu(education_level, population_count) VALUES
('Bilmiyor', 5386),
('Okuryazar Degil', 13142),
('Okuryazar Egitsiz', 65863),
('Ilkokul', 173949),
('Ortaokul', 148813),
('Ilkögretim', 69793),
('Lise', 198636),
('Lisans', 112939),
('Yüksek Lisans', 8764),
('Doktora', 1103);

-- Create Table Script
CREATE TABLE bursa_nilufer_edu (
    education_level_id SERIAL PRIMARY KEY,
    education_level VARCHAR(50) NOT NULL,
    population_count INT NOT NULL
);

-- Insert Data Script
INSERT INTO bursa_nilufer_edu (education_level, population_count) VALUES
('Bilmiyor', 2959),
('Okuryazar Degil', 3937),
('Okuryazar Egitsiz', 33358),
('Ilkokul', 66621),
('Ortaokul', 62827),
('Ilkögretim', 18166),
('Lise', 121977),
('Lisans', 134741),
('Yüksek Lisans', 19475),
('Doktora', 3009); 

-- Create Table Script
CREATE TABLE bursa_yildirim_edu (
    education_level_id SERIAL PRIMARY KEY,
    education_level VARCHAR(50) NOT NULL,
    population_count INT NOT NULL
);

-- Insert Data Script
INSERT INTO bursa_yildirim_edu(education_level, population_count) VALUES
('Bilmiyor', 9710),
('Okuryazar Degil', 12326),
('Okuryazar Egitsiz', 55291),
('Ilkokul', 129919),
('Ortaokul', 114880),
('Ilkögretim', 50895),
('Lise', 123893),
('Lisans', 72828),
('Yüksek Lisans', 4989),
('Doktora', 434);


-- Create the combined table
CREATE TABLE bursa_edu_combined AS
SELECT
    e.education_level,
    o.population_count AS osmangazi,
    n.population_count AS nilufer,
    y.population_count AS yildirim
FROM (
    -- Use distinct education levels from any table (they all match)
    SELECT DISTINCT education_level FROM bursa_osmangazi_edu
) e
LEFT JOIN bursa_osmangazi_edu o ON o.education_level = e.education_level
LEFT JOIN bursa_nilufer_edu n    ON n.education_level = e.education_level
LEFT JOIN bursa_yildirim_edu y   ON y.education_level = e.education_level;
