#!/bin/bash

views=(
vw_urban_vitality
vw_land_use
vw_spatial_diversity
vw_activity_summary
vw_activity_ranking
vw_sms_hotspots
vw_call_hotspots
vw_internet_hotspots
vw_business_zones
vw_residential_zones
vw_high_diversity
vw_dashboard
vw_map_data
vw_cell_summary
vw_kpi_summary
)

mkdir -p telepulse_csv

for view in "${views[@]}"
do
    hive --database telepulse \
    --showHeader=true \
    --outputformat=csv2 \
    -e "SELECT * FROM $view" \
    > telepulse_csv/$view.csv

    echo "$view exported"
done