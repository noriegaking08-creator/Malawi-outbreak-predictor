
import streamlit as st
import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.losses import MeanSquaredError
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import os
import joblib
from src.data.data_loader import load_data
from src.data.external_data import simulate_external_data

def pretrain_lstm(disease, external_data):
    merged = external_data[external_data['disease'] == disease].copy()
    merged['cases_lag1'] = merged.groupby('district')['cases'].shift(1)
    merged['rainfall_lag2'] = merged.groupby('district')['rainfall_mm'].shift(2)
    merged['future_cases'] = merged.groupby('district')['cases'].shift(-4)
    merged.dropna(inplace=True)

    features = ['cases_lag1', 'rainfall_lag2', 'temperature_c']
    X, y = [], []
    scaler = MinMaxScaler()
    for dist in merged['district'].unique():
        dist_data = merged[merged['district'] == dist][features]
        dist_target = merged[merged['district'] == dist]['future_cases']
        if len(dist_data) < 5:
            continue
        dist_data_scaled = scaler.fit_transform(dist_data)
        for i in range(len(dist_data) - 4):
            X.append(dist_data_scaled[i:i+4])
            y.append(dist_target.iloc[i+4])

    if len(X) == 0:
       # st.error(f"Insufficient external data for pre-training {disease} LSTM.")
        return None, scaler

    X, y = np.array(X), np.array(y)
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    model = Sequential([
        LSTM(50, activation='relu', input_shape=(4, 3), return_sequences=True),
        LSTM(25),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss=MeanSquaredError())
    model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_val, y_val), verbose=0)

    os.makedirs('data/models', exist_ok=True)
    model.save(f'data/models/pretrained_lstm_{disease}.h5')
    joblib.dump(scaler, f'data/models/pretrained_scaler_{disease}.pkl')
    return model, scaler

def finetune_lstm(disease, pretrained_model_path):
    disease_df, climate_df, _ = load_data()
    disease_df = disease_df[disease_df['disease'] == disease]
    merged = pd.merge(disease_df, climate_df, on=['district', 'date'])

    # Defensive check for rainfall_mm
    if 'rainfall_mm' not in merged.columns:
        #st.error("'rainfall_mm' column missing after merge. Check climate_df and merge keys.")
        print("Merged columns:", merged.columns.tolist())
        return None, None

    merged['cases_lag1'] = merged.groupby('district')['cases'].shift(1)
    merged['rainfall_lag2'] = merged.groupby('district')['rainfall_mm'].shift(2)
    merged['future_cases'] = merged.groupby('district')['cases'].shift(-4)
    merged.dropna(inplace=True)

    features = ['cases_lag1', 'rainfall_lag2', 'temperature_c']
    X, y = [], []
    scaler = MinMaxScaler()
    for dist in merged['district'].unique():
        dist_data = merged[merged['district'] == dist][features]
        dist_target = merged[merged['district'] == dist]['future_cases']
        if len(dist_data) < 5:
            continue
        dist_data_scaled = scaler.fit_transform(dist_data)
        for i in range(len(dist_data) - 4):
            X.append(dist_data_scaled[i:i+4])
            y.append(dist_target.iloc[i+4])

    if len(X) == 0:
        #st.error(f"Insufficient data for fine-tuning {disease} LSTM.")
        return None, scaler

    X, y = np.array(X), np.array(y)
    try:
        model = load_model(pretrained_model_path)
        scaler = joblib.load(f'data/models/pretrained_scaler_{disease}.pkl')
    except Exception as e:
       # st.error(f"Failed to load model: {e}. Training from scratch.")
        model = Sequential([
            LSTM(50, activation='relu', input_shape=(4, 3), return_sequences=True),
            LSTM(25),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss=MeanSquaredError())

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train, epochs=5, batch_size=32, validation_data=(X_val, y_val), verbose=0)
    model.save(f'data/models/finetuned_lstm_{disease}.h5')
    joblib.dump(scaler, f'data/models/finetuned_scaler_{disease}.pkl')
    return model, scaler

@st.cache_resource
def load_lstm_models(disease):
    pretrained_model_path = f'data/models/pretrained_lstm_{disease}.h5'
    if not os.path.exists(pretrained_model_path):
        #st.info(f"Pre-training LSTM for {disease}...")
        external_data = simulate_external_data(disease)
        model, scaler = pretrain_lstm(disease, external_data)
    else:
        model, scaler = finetune_lstm(disease, pretrained_model_path)
    return model, scaler
