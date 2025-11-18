import streamlit as st
import pandas as pd
from prophet import Prophet
import os
import json
from src.data.data_loader import load_data
from src.data.external_data import simulate_external_data
import logging
def pretrain_prophet(disease, external_data):
    """Pre-train Prophet on a larger dataset."""
    merged = external_data[external_data['disease'] == disease].copy()
    merged = merged.rename(columns={'date': 'ds', 'cases': 'y'})
    models = {}
    districts = [
        'Balaka', 'Blantyre', 'Chikwawa', 'Chiradzulu', 'Chitipa', 'Dedza', 'Dowa', 
        'Karonga', 'Kasungu', 'Likoma', 'Lilongwe', 'Machinga', 'Mangochi', 'Mchinji', 
        'Mulanje', 'Mwanza', 'Mzimba', 'Neno', 'Nkhata Bay', 'Nkhotakota', 'Nsanje', 
        'Ntcheu', 'Ntchisi', 'Phalombe', 'Rumphi', 'Salima', 'Thyolo', 'Zomba'
    ]
    for dist in merged['district'].unique():
        if dist not in districts:
           
            continue
        dist_data = merged[merged['district'] == dist][['ds', 'y', 'rainfall_mm', 'temperature_c']]
        if len(dist_data) < 10:
           
            continue
        try:
            model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
            model.add_regressor('rainfall_mm')
            model.add_regressor('temperature_c')
            model.fit(dist_data)
            models[dist] = model
        except Exception as e:
            logging.error(f"Failed to fit Prophet for {disease} in {dist}: {e}")
    os.makedirs('data/models', exist_ok=True)
    for dist, model in models.items():
        with open(f'data/models/pretrained_prophet_{disease}_{dist}.json', 'w') as f:
            json.dump(model_to_json(model), f)
    logging.info(f"Pre-trained Prophet models for {disease} in {len(models)} districts.")
    return models

def finetune_prophet(disease, pretrained_model_path=None):
    """Fine-tune Prophet on Malawi-specific data."""
    disease_df, climate_df, _ = load_data()
    disease_df = disease_df[disease_df['disease'] == disease]
    merged = pd.merge(disease_df, climate_df, on=['district', 'date'])
    merged = merged.rename(columns={'date': 'ds', 'cases': 'y'})
    models = {}
    districts = [
        'Balaka', 'Blantyre', 'Chikwawa', 'Chiradzulu', 'Chitipa', 'Dedza', 'Dowa', 
        'Karonga', 'Kasungu', 'Likoma', 'Lilongwe', 'Machinga', 'Mangochi', 'Mchinji', 
        'Mulanje', 'Mwanza', 'Mzimba', 'Neno', 'Nkhata Bay', 'Nkhotakota', 'Nsanje', 
        'Ntcheu', 'Ntchisi', 'Phalombe', 'Rumphi', 'Salima', 'Thyolo', 'Zomba'
    ]
    for dist in merged['district'].unique():
        if dist not in districts:
            logging.warning(f"Skipping unknown district {dist} in fine-tuning.")
            continue
        dist_data = merged[merged['district'] == dist][['ds', 'y', 'rainfall_mm', 'temperature_c']]
        if len(dist_data) < 10:
            logging.warning(f"Skipping {dist} for {disease}: only {len(dist_data)} rows.")
            continue
        try:
            with open(f'data/models/pretrained_prophet_{disease}_{dist}.json', 'r') as f:
                model = model_from_json(json.load(f))
        except FileNotFoundError:
            logging.warning(f"No pretrained model for {disease} in {dist}. Training from scratch.")
            model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
            model.add_regressor('rainfall_mm')
            model.add_regressor('temperature_c')
        try:
            model.fit(dist_data)
            models[dist] = model
        except Exception as e:
            logging.error(f"Failed to fine-tune Prophet for {disease} in {dist}: {e}")
    os.makedirs('data/models', exist_ok=True)
    for dist, model in models.items():
        with open(f'data/models/finetuned_prophet_{disease}_{dist}.json', 'w') as f:
            json.dump(model_to_json(model), f)
    logging.info(f"Fine-tuned Prophet models for {disease} in {len(models)} districts.")
    return models

@st.cache_resource
def load_prophet_models(disease):
    """Load or train Prophet models with fine-tuning."""
    districts = [
        'Balaka', 'Blantyre', 'Chikwawa', 'Chiradzulu', 'Chitipa', 'Dedza', 'Dowa', 
        'Karonga', 'Kasungu', 'Likoma', 'Lilongwe', 'Machinga', 'Mangochi', 'Mchinji', 
        'Mulanje', 'Mwanza', 'Mzimba', 'Neno', 'Nkhata Bay', 'Nkhotakota', 'Nsanje', 
        'Ntcheu', 'Ntchisi', 'Phalombe', 'Rumphi', 'Salima', 'Thyolo', 'Zomba'
    ]
    pretrained_exists = all(os.path.exists(f'data/models/pretrained_prophet_{disease}_{dist}.json') for dist in districts)
    if not pretrained_exists:
        logging.info(f"Pre-training Prophet for {disease}...")
        external_data = simulate_external_data(disease)
        models = pretrain_prophet(disease, external_data)
    else:
        models = finetune_prophet(disease)
    return models

def model_to_json(model):
    """Convert Prophet model to JSON."""
    from prophet.serialize import model_to_json
    return model_to_json(model)

def model_from_json(json_str):
    """Load Prophet model from JSON."""
    from prophet.serialize import model_from_json
    return model_from_json(json_str)


def storing_logs():
    return logging.basicConfig(filename='data/logs/prophet_training.txt', level=logging.WARNING) and logging.warning('This is a warning message for Prophet model training.')
storing_logs()




