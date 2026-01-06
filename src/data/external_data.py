import pandas as pd
import numpy as np

def simulate_external_data(disease, num_samples=10000):
    """Simulate a larger dataset for pre-training (replaceable with real data, e.g., WHO)."""
    districts = ['Blantyre', 'Lilongwe', 'Mangochi','Zomba', 'Chiradzulu', 'Thyolo', 'Nsanje', 'Mulanje',
                'Chikwawa', 'Salima', 'Nkhotakota', 'Karonga', 'Chitipa', 'Rumphi', 'Dedza', 'Dowa', 'Kasungu',
                'Mchinji', 'Ntcheu', 'Balaka', 'Machinga', 'Phalombe', 'Mwanza', 'Neno', 'Ntchisi', 'Likoma']
    dates = pd.date_range(start='2020-01-01', end='2025-10-17', freq='W')
    external_data = []
    for dist in districts:
        num_dates = len(dates)
        if disease == 'Malaria':
            cases = np.random.poisson(500, num_dates) + np.random.normal(0, 100, num_dates).astype(int)
        elif disease == 'Cholera':
            cases = np.random.poisson(200, num_dates) + np.random.normal(0, 50, num_dates).astype(int)
        else:  
            cases = np.random.poisson(50, num_dates) + np.random.normal(0, 20, num_dates).astype(int)
        df = pd.DataFrame({
            'district': dist,
            'date': dates,
            'cases': cases,
            'disease': disease,
            'rainfall_mm': np.random.uniform(10, 150, num_dates),
            'temperature_c': np.random.uniform(20, 35, num_dates)
        })
        external_data.append(df)
    return pd.concat(external_data)