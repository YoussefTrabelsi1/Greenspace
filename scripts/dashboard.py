import streamlit as st
import pandas as pd
import plotly.express as px
import pyproj
import warnings

warnings.filterwarnings('ignore')


# Coordinate transformation
inProj = pyproj.Proj("+init=EPSG:3945")
outProj = pyproj.Proj("+init=EPSG:4326")

def transform(x, y):
    """Transform coordinates from EPSG:3945 to EPSG:4326."""
    x2, y2 = pyproj.transform(inProj, outProj, x, y)
    return y2, x2

def load_and_transform_data(data_path):
    """Load and transform tree dataset."""
    data = pd.read_csv(data_path)
    data = data.sample(frac=0.02, random_state=42)
    # Apply coordinate transformation
    transformed_coords = data.apply(
        lambda row: transform(row['coord_x'], row['coord_y']),
        axis=1
    )
    data['lat'], data['lon'] = zip(*transformed_coords)
    
    return data

# File paths
data_path = "data/raw/donnees-defi-egc.csv"

# Load and transform data
data = load_and_transform_data(data_path)

# Streamlit dashboard
st.title("Grenoble Tree Park Insights 🌳")
st.sidebar.title("Navigation")

# Section 1: Interactive Map
st.header("Interactive Map of Trees")
st.markdown("Explore the tree locations in Grenoble with additional details.")
fig_map = px.scatter_mapbox(
    data,
    lat="lat",
    lon="lon",
    color="VIGUEUR",
    size_max=15,
    zoom=12,
    hover_data=["ESPECE", "DIAMETREARBREAUNMETRE"],
    mapbox_style="open-street-map"
)
st.plotly_chart(fig_map)

# Section 2: Tree Defects
st.header("Tree Defects Distribution")
st.markdown("Analyze the distribution of tree defects in Grenoble.")
defect_cols = ["Collet", "Houppier", "Racine", "Tronc"]
defect_counts = data[defect_cols].sum()
fig_defects = px.pie(
    names=defect_counts.index,
    values=defect_counts.values,
    title="Defect Distribution by Type"
)
st.plotly_chart(fig_defects)

# Section 3: Temporal Trends
st.header("Temporal Trends")
st.markdown("Observe the evolution of tree plantations over the years.")
data['ANNEEDEPLANTATION'] = pd.to_numeric(data['ANNEEDEPLANTATION'], errors='coerce')
annual_planting = data.groupby('ANNEEDEPLANTATION').size().reset_index(name='count')
fig_trend = px.line(
    annual_planting,
    x='ANNEEDEPLANTATION',
    y='count',
    title="Number of Trees Planted Over Time",
    labels={"ANNEEDEPLANTATION": "Year", "count": "Number of Trees"}
)
st.plotly_chart(fig_trend)
