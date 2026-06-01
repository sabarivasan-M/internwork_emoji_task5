"""
Run sensitivity analysis for clustering parameter `n_clusters`.
Generates `recommended_locations_n{n}.csv` and `sensitivity_map_n{n}.png` for each tested n.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
from geospatial_analysis import load_data, cluster_demand, score_clusters

OUT_DIR = os.path.dirname(__file__) + '/'

def plot_map(demand, stores, comps, rec, out_png):
    plt.figure(figsize=(10,6))
    # demand points sized by demand_score
    s = (demand['demand_score'] - demand['demand_score'].min()) + 1
    plt.scatter(demand['lon'], demand['lat'], c='lightgray', s= (s.clip(0,100)), alpha=0.6, label='demand')
    # stores
    if len(stores):
        plt.scatter(stores['lon'], stores['lat'], c='blue', s=30, marker='^', label='stores')
    # competitors
    if len(comps):
        plt.scatter(comps['lon'], comps['lat'], c='black', s=10, marker='x', label='competitors')
    # recommended
    plt.scatter(rec['lon'], rec['lat'], c='red', s=120, marker='o', edgecolor='k', label='recommended')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Sensitivity map')
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    plt.close()


def run():
    demand, stores, comps = load_data()
    n_list = [30,50,70,100]
    summary = []
    for n in n_list:
        d2, centers = cluster_demand(demand.copy(), n_clusters=n)
        clusters = score_clusters(d2, centers, stores, comps)
        rec = clusters[(clusters['nearest_store_km']>=30)].head(12)
        csv_out = OUT_DIR + f'recommended_locations_n{n}.csv'
        rec.to_csv(csv_out, index=False)
        png_out = OUT_DIR + f'sensitivity_map_n{n}.png'
        plot_map(d2, stores, comps, rec, png_out)
        print(f"✓ n_clusters={n}: saved {csv_out} and {png_out}")
        summary.append({'n_clusters':n,'top1_cluster':rec.iloc[0]['cluster'] if len(rec) else None,'top1_score':rec.iloc[0]['score'] if len(rec) else None})
    pd.DataFrame(summary).to_csv(OUT_DIR + 'sensitivity_summary.csv', index=False)
    print('\nSensitivity analysis complete. Summary saved to sensitivity_summary.csv')

if __name__ == '__main__':
    run()
