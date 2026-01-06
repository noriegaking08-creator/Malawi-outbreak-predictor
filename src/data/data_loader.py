import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np

@st.cache_data(ttl=3600)
def load_data():
    """Load and validate data from CSV for health reports and simulated climate data."""
    districts = [
        'Balaka', 'Blantyre', 'Chikwawa', 'Chiradzulu', 'Chitipa', 'Dedza', 'Dowa', 
        'Karonga', 'Kasungu', 'Likoma', 'Lilongwe', 'Machinga', 'Mangochi', 'Mchinji', 
        'Mulanje', 'Mwanza', 'Mzimba', 'Neno', 'Nkhata Bay', 'Nkhotakota', 'Nsanje', 
        'Ntcheu', 'Ntchisi', 'Phalombe', 'Rumphi', 'Salima', 'Thyolo', 'Zomba'
    ]
    diseases = ['Malaria', 'Cholera', 'Monkeypox']

    try:
        disease_df = pd.read_csv('data/malawi_health_data.csv')
        required_cols = ['district', 'date', 'cases', 'disease', 'rainfall_mm', 'temperature_c']
        missing = [col for col in required_cols if col not in disease_df.columns]
        if missing:
      
            raise ValueError("Invalid columns in CSV")
        disease_df['date'] = pd.to_datetime(disease_df['date'])
        if (disease_df['cases'] < 0).any():
            st.warning("Negative cases detected. Imputing...")
            disease_df['cases'] = disease_df['cases'].clip(lower=0)
    except Exception as e:
      
        dates = pd.date_range(start='2024-01-01', end='2025-10-13', freq='W-MON')
        disease_data = []
        for disease in diseases:
            for dist in districts:
                num_dates = len(dates)
                cases = np.random.randint(100, 1500, num_dates) if disease == 'Malaria' else np.random.randint(50, 700, num_dates) if disease == 'Cholera' else np.random.randint(10, 200, num_dates)
                rainfall = np.random.uniform(0, 250, num_dates)
                temp = np.random.uniform(15, 35, num_dates)
                df = pd.DataFrame({
                    'district': [dist] * num_dates,
                    'date': dates,
                    'cases': cases,
                    'disease': [disease] * num_dates,
                    'rainfall_mm': rainfall,
                    'temperature_c': temp
                })
                disease_data.append(df)
        disease_df = pd.concat(disease_data)

    climate_df = disease_df[['district', 'date', 'rainfall_mm', 'temperature_c']].drop_duplicates()

    try:
        gpd.options.io_engine = 'fiona'
        gdf = gpd.read_file('data/malawi_districts.geojson', driver='GeoJSON')
        if 'shapeName' not in gdf.columns:
            if 'shapeISO' in gdf.columns:
                gdf['shapeName'] = gdf['shapeISO']
            elif 'name' in gdf.columns:
                gdf['shapeName'] = gdf['name']
            else:
                gdf['shapeName'] = gdf.index.astype(str)  # Use index as default names
        # Ensure the gdf has a CRS set (WGS84 is standard for geographic coordinates)
        if gdf.crs is None:
            gdf.set_crs(epsg=4326, inplace=True)  # Set default CRS for WGS84
        if not all(d in gdf['shapeName'].values for d in districts):
            # If districts don't match, create a new GeoDataFrame with proper districts
            gdf = gpd.GeoDataFrame({'shapeName': districts}, geometry=[None] * len(districts))
            gdf.set_crs(epsg=4326, inplace=True)  # Set default CRS for WGS84
    except Exception as e:

        gdf = gpd.GeoDataFrame({'shapeName': districts}, geometry=[None] * len(districts))
        gdf.set_crs(epsg=4326, inplace=True)  # Set default CRS for WGS84

    return disease_df, climate_df, gdf
