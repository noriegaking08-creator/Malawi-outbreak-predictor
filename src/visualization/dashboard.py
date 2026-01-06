import streamlit as st
import plotly.express as px

def render_dashboard(disease_df, climate_df, diseases):
    st.header("📊 Dashboard")
    st.markdown("### Disease Overview")
    
   
    for disease in diseases:
        filtered_df = disease_df[disease_df['disease'] == disease]
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(f"Total {disease} Cases", f"{filtered_df['cases'].sum():,}")
        with col2:
            st.metric(f"Avg Weekly {disease} Cases", f"{filtered_df['cases'].mean():.1f}")
        with col3:
            threshold = 600 if disease == 'Malaria' else 200 if disease == 'Cholera' else 50
            st.metric(f"High-Risk Districts ({disease})", 
                      len(filtered_df[filtered_df['cases'] > threshold]['district'].unique()))
        
        
        fig = px.line(filtered_df, x='date', y='cases', color='district', 
                      title=f"Historical {disease} Cases")
        st.plotly_chart(fig, use_container_width=True)
    
   
    st.markdown("### Climate Overview")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Avg Rainfall (mm/week)", f"{climate_df['rainfall_mm'].mean():.1f}")
    with col2:
        st.metric("Avg Temperature (°C)", f"{climate_df['temperature_c'].mean():.1f}")