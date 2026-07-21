-- TelePulse Validation Script
-- Validates warehouse objects after Spark pipeline

USE telepulse;

-- Tables
SHOW TABLES;

DESCRIBE urban_vitality;
DESCRIBE land_use_classification;
DESCRIBE spatial_diversity;

-- Row Counts
SELECT COUNT(*) AS urban_vitality_rows
FROM urban_vitality;

SELECT COUNT(*) AS land_use_rows
FROM land_use_classification;

SELECT COUNT(*) AS spatial_diversity_rows
FROM spatial_diversity;

-- Sample Data
SELECT *
FROM urban_vitality
LIMIT 10;

SELECT *
FROM land_use_classification
LIMIT 10;

SELECT *
FROM spatial_diversity
LIMIT 10;

-- Views
SHOW VIEWS;

-- Dashboard Views
SELECT *
FROM vw_dashboard
LIMIT 10;

SELECT *
FROM vw_map_data
LIMIT 10;

SELECT *
FROM vw_cell_summary
LIMIT 10;

-- KPI Views
SELECT *
FROM vw_kpi_summary;

-- Hotspot Views
SELECT *
FROM vw_activity_ranking
ORDER BY urban_vitality_index DESC
LIMIT 10;

SELECT *
FROM vw_internet_hotspots
ORDER BY total_internet DESC
LIMIT 10;

SELECT *
FROM vw_sms_hotspots
ORDER BY total_sms DESC
LIMIT 10;

SELECT *
FROM vw_call_hotspots
ORDER BY total_calls DESC
LIMIT 10;

-- Zone Distribution
SELECT
    land_use_category,
    COUNT(*) AS total_cells
FROM land_use_classification
GROUP BY land_use_category;

-- Spatial Diversity
SELECT *
FROM vw_high_diversity
ORDER BY shannon_entropy_diversity_index DESC
LIMIT 10;