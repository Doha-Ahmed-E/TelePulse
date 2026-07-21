-- TelePulse Analytical Views
-- Creates analytical views for the dashboard

USE telepulse;

-- Base Views --

-- Urban Vitality
CREATE OR REPLACE VIEW vw_urban_vitality AS
SELECT
    cellid,
    total_sms_in,
    total_sms_out,
    total_call_in,
    total_call_out,
    total_internet,
    urban_vitality_index
FROM urban_vitality;


-- Land Use Classification
CREATE OR REPLACE VIEW vw_land_use AS
SELECT
    cellid,
    total_business,
    total_residential,
    land_use_category
FROM land_use_classification;


-- Spatial Diversity
CREATE OR REPLACE VIEW vw_spatial_diversity AS
SELECT
    cellid,
    shannon_entropy_diversity_index
FROM spatial_diversity;


-- Activity Analysis Views --

-- Activity Summary
CREATE OR REPLACE VIEW vw_activity_summary AS
SELECT

    cellid,

    total_sms_in + total_sms_out AS total_sms,

    total_call_in + total_call_out AS total_calls,

    total_internet,

    urban_vitality_index

FROM urban_vitality;


-- Activity Ranking
CREATE OR REPLACE VIEW vw_activity_ranking AS
SELECT

    cellid,

    urban_vitality_index,

    total_sms_in,

    total_sms_out,

    total_call_in,

    total_call_out,

    total_internet

FROM urban_vitality;


-- SMS Hotspots
CREATE OR REPLACE VIEW vw_sms_hotspots AS
SELECT

    cellid,

    total_sms_in,

    total_sms_out,

    total_sms_in + total_sms_out AS total_sms

FROM urban_vitality;


-- Call Hotspots
CREATE OR REPLACE VIEW vw_call_hotspots AS
SELECT

    cellid,

    total_call_in,

    total_call_out,

    total_call_in + total_call_out AS total_calls

FROM urban_vitality;


-- Internet Hotspots
CREATE OR REPLACE VIEW vw_internet_hotspots AS
SELECT

    cellid,

    total_internet,

    urban_vitality_index

FROM urban_vitality;


-- Land Use Views --

-- Business Zones
CREATE OR REPLACE VIEW vw_business_zones AS
SELECT *

FROM land_use_classification

WHERE land_use_category = 'Business/Office';


-- Residential Zones
CREATE OR REPLACE VIEW vw_residential_zones AS
SELECT *

FROM land_use_classification

WHERE land_use_category = 'Residential';


-- Spatial Analysis Views --

-- High Spatial Diversity
CREATE OR REPLACE VIEW vw_high_diversity AS
SELECT

    cellid,

    shannon_entropy_diversity_index

FROM spatial_diversity;


-- Dashboard Views --

-- Dashboard View (Complete Dataset)
CREATE OR REPLACE VIEW vw_dashboard AS
SELECT

    u.cellid,

    u.total_sms_in,
    u.total_sms_out,
    u.total_call_in,
    u.total_call_out,
    u.total_internet,
    u.urban_vitality_index,

    l.total_business,
    l.total_residential,
    l.land_use_category,

    s.shannon_entropy_diversity_index

FROM vw_urban_vitality u

LEFT JOIN vw_land_use l
ON u.cellid = l.cellid

LEFT JOIN vw_spatial_diversity s
ON u.cellid = s.cellid;


-- Dashboard Map View
CREATE OR REPLACE VIEW vw_map_data AS
SELECT

    u.cellid,

    u.urban_vitality_index,

    u.total_internet,

    l.land_use_category,

    s.shannon_entropy_diversity_index

FROM urban_vitality u

JOIN land_use_classification l
ON u.cellid = l.cellid

JOIN spatial_diversity s
ON u.cellid = s.cellid;


-- Dashboard Summary per Cell
CREATE OR REPLACE VIEW vw_cell_summary AS
SELECT

    u.cellid,

    u.urban_vitality_index,

    u.total_internet,

    (u.total_sms_in + u.total_sms_out) AS total_sms,

    (u.total_call_in + u.total_call_out) AS total_calls,

    l.land_use_category,

    s.shannon_entropy_diversity_index

FROM urban_vitality u

JOIN land_use_classification l
ON u.cellid = l.cellid

JOIN spatial_diversity s
ON u.cellid = s.cellid;


-- KPI Views --

-- Dataset KPI Summary
CREATE OR REPLACE VIEW vw_kpi_summary AS
SELECT

    COUNT(*) AS total_cells,

    SUM(total_sms_in + total_sms_out) AS total_sms,

    SUM(total_call_in + total_call_out) AS total_calls,

    SUM(total_internet) AS total_internet,

    AVG(urban_vitality_index) AS average_urban_vitality,

    MAX(urban_vitality_index) AS maximum_urban_vitality,

    AVG(total_internet) AS average_internet_usage

FROM urban_vitality;