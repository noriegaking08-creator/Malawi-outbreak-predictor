import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import numpy as np
import logging

logging.basicConfig(filename='data/logs/prediction_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

def render_map_view(disease_df, climate_df, gdf, diseases, model_type, lstm_models, prophet_models):
    st.header("🗺️ District Risk Map")
    disease = st.selectbox("Select Disease for Map", diseases)
    with st.spinner("Generating predictions..."):
        pred_df = pd.DataFrame()
        for dist in disease_df['district'].unique():
            if model_type == "LSTM":
                model, scaler = lstm_models[disease]
                if model is None:
                    continue
                latest = pd.merge(disease_df[(disease_df['district'] == dist) & (disease_df['disease'] == disease)].tail(4), 
                                 climate_df[climate_df['district'] == dist].tail(4), 
                                 on=['district', 'date'])
                if len(latest) < 4:
                    continue
                features = latest[['cases', 'rainfall_mm', 'temperature_c']].values
                features_scaled = scaler.transform(features)
                pred_cases = model.predict(features_scaled[np.newaxis, ...], verbose=0)[0, 0]
            else:
                models = prophet_models[disease]
                if dist not in models:
                    continue
                m = models[dist]
                future = m.make_future_dataframe(periods=4, freq='W')
                last_rain = climate_df[climate_df['district'] == dist]['rainfall_mm'].iloc[-1]
                last_temp = climate_df[climate_df['district'] == dist]['temperature_c'].iloc[-1]
                future['rainfall_mm'] = last_rain
                future['temperature_c'] = last_temp
                forecast = m.predict(future)
                pred_cases = forecast['yhat'].iloc[-1]
            pred_cases = max(0, pred_cases)
            risk = "Low" if pred_cases < (300 if disease == 'Malaria' else 100 if disease == 'Cholera' else 25) else \
                   "Medium" if pred_cases < (600 if disease == 'Malaria' else 200 if disease == 'Cholera' else 50) else "High"
            pred_df = pd.concat([pred_df, pd.DataFrame({
                'district': [dist], 'predicted_cases': [pred_cases], 'risk': [risk], 'disease': [disease]
            })], ignore_index=True)
            logging.info(f"Prediction for {dist} ({disease}): {pred_cases:.0f} cases, Risk: {risk}")
        
        pred_gdf = gdf.merge(pred_df, left_on='shapeName', right_on='district', how='left')
        pred_gdf['risk_score'] = pd.to_numeric(pred_gdf['predicted_cases'], errors='coerce').fillna(0)
        
        m = folium.Map(location=[-13.5, 34], zoom_start=7, tiles="cartodbpositron")
        folium.Choropleth(
            geo_data=pred_gdf,
            name="Risk",
            data=pred_gdf,
            columns=["district", "risk_score"],
            key_on="feature.properties.shapeName",
            fill_color="RdYlGn_r",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=f"Predicted {disease} Cases (4 Weeks)"
        ).add_to(m)
        folium.LayerControl().add_to(m)
        st_folium(m, width=700, height=500)