"""
Geospatial Analysis for Business Expansion
Clusters demand points, computes cluster demand, evaluates proximity to existing stores,
and identifies high-demand low-presence regions as expansion recommendations.
Produces `recommended_locations.csv` and `expansion_map.html`.
"""
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import math

# haversine distance (km)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)
    a = np.sin(dphi/2.0)**2 + np.cos(phi1)*np.cos(phi2)*np.sin(dlambda/2.0)**2
    return R * 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

def load_data(base_path="c:/Users/HP/Music/data_anal_inter/task4/"):
    demand = pd.read_csv(base_path + 'demand_points.csv')
    stores = pd.read_csv(base_path + 'existing_stores.csv')
    comps = pd.read_csv(base_path + 'competitors.csv')
    return demand, stores, comps

def cluster_demand(demand, n_clusters=60):
    coords = demand[['lat','lon']].values
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(coords)
    demand['cluster'] = labels
    centers = pd.DataFrame(kmeans.cluster_centers_, columns=['lat','lon'])
    return demand, centers

def score_clusters(demand, centers, stores, comps):
    clusters = demand.groupby('cluster').agg(
        total_demand=('demand_score','sum'),
        population=('population','sum'),
        count_points=('point_id','count')
    ).reset_index()
    clusters = clusters.merge(centers.reset_index().rename(columns={'index':'cluster'}), on='cluster')

    # compute distance to nearest own store and competitor density
    nearest_store_km = []
    comp_count_within50 = []
    for _, row in clusters.iterrows():
        lat = row['lat']; lon = row['lon']
        if len(stores)>0:
            dists = haversine(lat, lon, stores['lat'].values, stores['lon'].values)
            nearest_store_km.append(dists.min())
        else:
            nearest_store_km.append(np.nan)
        # competitor density within 50 km
        dcomp = haversine(lat, lon, comps['lat'].values, comps['lon'].values)
        comp_count_within50.append((dcomp <= 50).sum())

    clusters['nearest_store_km'] = nearest_store_km
    clusters['competitors_within_50km'] = comp_count_within50
    clusters['score'] = clusters['total_demand'] / (1 + clusters['competitors_within_50km'])
    clusters = clusters.sort_values('score', ascending=False)
    return clusters

def recommend_locations(clusters, top_n=10, min_distance_km=30):
    # select clusters with high score and distance from nearest store greater than min_distance_km
    candidates = clusters[(clusters['nearest_store_km'] >= min_distance_km)].copy()
    rec = candidates.head(top_n)
    return rec

def save_recommendations(rec, out_csv=r"c:\Users\HP\Music\data_anal_inter\task4\recommended_locations.csv"):
    rec.to_csv(out_csv, index=False)
    print(f"✓ Saved recommendations: {out_csv}")

def generate_map(rec, stores, comps, out_html=r"c:\Users\HP\Music\data_anal_inter\task4\expansion_map.html"):
    # Create a simple Leaflet map embedding markers
    markers_js = []
    for _, r in rec.iterrows():
        markers_js.append(f"L.circle([{r['lat']:.6f}, {r['lon']:.6f}], {{color:'red', radius:50000}}).bindPopup('Recommended: score={r['score']:.1f}<br>nearest_store_km={r['nearest_store_km']:.1f}');")
    for _, s in stores.iterrows():
        markers_js.append(f"L.marker([{s['lat']:.6f}, {s['lon']:.6f}], {{icon: L.icon({{iconUrl:'https://maps.gstatic.com/mapfiles/ms2/micons/blue.png',iconSize:[24,24]}})}}).bindPopup('Store: {s.get('store_id','') }');")
    for _, c in comps.iterrows():
        markers_js.append(f"L.marker([{c['lat']:.6f}, {c['lon']:.6f}], {{icon: L.icon({{iconUrl:'https://maps.gstatic.com/mapfiles/ms2/micons/red-dot.png',iconSize:[12,12]}})}}).bindPopup('Competitor: {c.get('competitor_id','') }');")

    markers_block = "\\n    ".join(markers_js)
    html = f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Expansion Map</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css"/>
  <style>#map{{height:90vh;width:100%}}</style>
</head>
<body>
  <div id="map"></div>
  <script src="https://unpkg.com/leaflet@1.9.3/dist/leaflet.js"></script>
  <script>
    var map = L.map('map').setView([39.5, -98.35], 4);
    L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{maxZoom:18}}).addTo(map);
        { markers_block }
  </script>
</body>
</html>
"""
    with open(out_html, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✓ Map generated: {out_html}")

if __name__ == '__main__':
    demand, stores, comps = load_data()
    demand, centers = cluster_demand(demand, n_clusters=70)
    clusters = score_clusters(demand, centers, stores, comps)
    rec = recommend_locations(clusters, top_n=12, min_distance_km=50)
    save_recommendations(rec)
    generate_map(rec, stores, comps)
    print('\nTop recommended locations:')
    print(rec[['cluster','lat','lon','total_demand','nearest_store_km','competitors_within_50km','score']].head(12))
