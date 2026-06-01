# Geospatial Analysis Report — Business Expansion Recommendations

## Summary
- Goal: identify high-demand, low-presence regions for new store expansion.
- Inputs: `demand_points.csv`, `existing_stores.csv`, `competitors.csv` (generated).
- Outputs: `recommended_locations.csv`, `expansion_map.html` (interactive map), this report.

## Methodology
1. Cluster demand points using KMeans on latitude/longitude (n=70 clusters).
2. Aggregate cluster demand (`demand_score`) and population.
3. Compute nearest existing store distance (km) and competitor count within 50 km.
4. Score = total_demand / (1 + competitors_within_50km); prioritize clusters with high score and nearest store distance >= 50 km.

## Key Outputs
- Recommended locations (CSV): [task4/recommended_locations.csv](task4/recommended_locations.csv#L1)
- Interactive map: [task4/expansion_map.html](task4/expansion_map.html#L1)
- Scripts used: [task4/geospatial_analysis.py](task4/geospatial_analysis.py#L1), [task4/geospatial_sensitivity.py](task4/geospatial_sensitivity.py#L1)

## Top 6 Recommendations (from analysis)
1. Cluster 28 — lat 30.555257, lon -114.029169 — total_demand 44191.4 — nearest_store_km 427.32 — competitors 0
2. Cluster 30 — lat 40.186080, lon -106.890961 — total_demand 40155.1 — nearest_store_km 131.21 — competitors 0
3. Cluster 12 — lat 34.943702, lon -110.720225 — total_demand 33861.6 — nearest_store_km 291.49 — competitors 0
4. Cluster 52 — lat 43.124741, lon -115.821881 — total_demand 32758.2 — nearest_store_km 213.18 — competitors 0
5. Cluster 47 — lat 31.399992, lon -93.348333 — total_demand 32093.1 — nearest_store_km 382.04 — competitors 0
6. Cluster 63 — lat 26.357704, lon -91.132255 — total_demand 31991.4 — nearest_store_km 312.59 — competitors 0

(Full ranked list available in the CSV linked above.)

## Recommendations
- Prioritize top clusters by a combination of `score` and `nearest_store_km` (we used min 50 km threshold).
- Run on-the-ground validation for top 5 locations: market visits, local demographic checks, lease availability.
- Consider competitor presence (0 in top clusters here) and transportation access before committing.

## Next steps (optional)
- Run sensitivity analysis on `n_clusters` and `min_distance_km` and compare results.
- Produce zoomed-in maps and static PNGs for presentations.
- Incorporate road-network travel time (drive-time isochrones) instead of straight-line distance for more accurate catchment areas.

## Sensitivity Analysis Performed
- Sensitivity results currently available in the folder:
	- `recommended_locations_n70.csv`
	- `sensitivity_map_n70.png`
	- `sensitivity_summary.csv`

These outputs show the ranked recommendations and a stability snapshot for the selected `n_clusters = 70` run in this synthetic dataset.

---
Generated with `geospatial_analysis.py` in `task4`.
