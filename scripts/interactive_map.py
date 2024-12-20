import folium
import pandas as pd
import warnings
import pyproj
from tqdm import tqdm
warnings.filterwarnings('ignore')

# Coordinate transformation
inProj = pyproj.Proj("+init=EPSG:3945")
outProj = pyproj.Proj("+init=EPSG:4326")

def transform(x, y):
    """Transform coordinates from EPSG:3945 to EPSG:4326."""
    x2, y2 = pyproj.transform(inProj, outProj, x, y)
    return y2, x2

def create_interactive_map(data_path, output_path, sample_fraction=0.01):
    """Create an interactive map with a sampled dataset."""
    # Load dataset
    data = pd.read_csv(data_path)

    # Sample 1/100th of the trees
    data_sampled = data.sample(frac=sample_fraction, random_state=42)


    # Initialize the map centered on Grenoble
    map_gre = folium.Map(location=[45.1885, 5.7245], zoom_start=12)

    # Add tree markers
    for _, row in tqdm(data_sampled.iterrows()):
        try:
            # Transform coordinates
            coord_y, coord_x = transform(float(row['coord_x']), float(row['coord_y']))
            
            # Popup information
            popup_info = (
                f"Species: {row['ESPECE']}<br>"
                f"Diameter: {row['DIAMETREARBREAUNMETRE']}<br>"
                f"Health: {row['VIGUEUR']}"
            )
            
            # Add marker
            folium.Marker(
                [coord_y, coord_x],
                popup=popup_info,
                icon=folium.Icon(color="green" if row['VIGUEUR'] == "vigoureux" else "red"),
            ).add_to(map_gre)
        except (ValueError, TypeError):
            # Skip rows with invalid coordinates
            continue

    # Save map to HTML
    map_gre.save(output_path)
    print(f"Interactive map saved at: {output_path}")

if __name__ == "__main__":
    # File paths
    data_path = "data/raw/donnees-defi-egc.csv"
    output_path = "outputs/tree_map.html"

    # Create and save interactive map
    create_interactive_map(data_path, output_path, sample_fraction=0.02)
