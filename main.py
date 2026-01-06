import streamlit as st
import json
import os
from PIL import Image

USER_FILE = "data/users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def authenticate(username, password):
    users = load_users()
    return username in users and users[username]["password"] == password

def create_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = {"password": password}
    save_users(users)
    return True


st.markdown("""
    <style>
    .main {background-color: #f0f8f0;}
    .stApp {background: linear-gradient(to bottom, skyblue, #87CEEB);}
    .sidebar .sidebar-content {background-color: skyblue; color: white;}
    .stButton > button {background-color: blue; color: white; border-radius: 0.5rem;}
    h1, h2 {color: skyblue; text-align: center;}
    .metric-container {background-color: #87CEEB; padding: 1rem; border-radius: 0.5rem;}
    .stAlert {background-color: #FFF0F0; border: 1px solid #DC143C;}
    .title-text { 
        position: absolute; 
        top: 10%; 
        left: 50%; 
        transform: translate(-50%, -50%); 
        color: white; 
        font-family: Impact, sans-serif; 
        font-size: 48px; 
        font-weight: bold; 
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title(" Login to Access Malawi Outbreak Predictor")
    login_tab, signup_tab = st.tabs([" LOGIN", "CREATE ACCOUNT"])

    with login_tab:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.success(f"Welcome back, {username}!")
                st.rerun()
            else:
                st.error("Invalid credentials. Try again or create a new account.")

    with signup_tab:
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")
        if st.button("Create Account"):
            if create_user(new_user, new_pass):
                st.success("Account created! You can now log in.")
            else:
                st.warning("Username already exists. Try another.")
    st.stop()


st.title(" Malawi Outbreak Predictor")
st.markdown("---")

from src.visualization.dashboard import render_dashboard
from src.visualization.map_view import render_map_view
from src.visualization.predictions import render_predictions
from src.visualization.feedback import render_feedback
from src.data.data_loader import load_data
from src.models.istm_model import load_lstm_models
from src.models.prophet_model import load_prophet_models


model_type = "Prophet"
with st.spinner("PROCESSING FEW ONLINE INFORMATION..."):
    disease_df, climate_df, gdf = load_data()
    diseases = ['Malaria', 'Cholera', 'Monkeypox']
    lstm_models = {disease: load_lstm_models(disease) for disease in diseases}
    prophet_models = {disease: load_prophet_models(disease) for disease in diseases}


tab1, tab2, tab3, tab4 = st.tabs([" DASHBOARD", " MAP VIEW", " PREDICTIONS", " FEEDBACK"])

with tab1:
    st.subheader("Dashboard Overview")
    try:
        image = Image.open('data/images/black_doctor.png')
        st.image(image, use_container_width=True)
    except:
        st.error("Image not found.")
    render_dashboard(disease_df, climate_df, diseases)

with tab2:
    render_map_view(disease_df, climate_df, gdf, diseases, model_type, lstm_models, prophet_models)

with tab3:
    render_predictions(disease_df, climate_df, diseases, model_type, lstm_models, prophet_models)

with tab4:
    render_feedback()




