import streamlit as st
import pandas as pd
import numpy as np
import pickle
import json
from datetime import datetime

st.set_page_config(page_title="India House Price Predictor", page_icon="🏠", layout="wide")

@st.cache_resource
def load_artifacts():
    with open("house_price_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("feature_info.json", "r") as f:
        feature_info = json.load(f)
    return model, feature_info

model, feature_info = load_artifacts()
feature_names = feature_info["feature_names"]
cities = feature_info["cities"]

if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.header("Model Info")
    st.markdown("**Model:** trained on 6 Indian metro cities  \n**Target:** log-transformed price (converted back to INR for display)  \n**Cities:** " + ", ".join(cities))
    st.divider()
    st.header("Session History")
    if st.session_state.history:
        for h in reversed(st.session_state.history[-10:]):
            st.write(f"`{h['time']}` — {h['summary']}")
    if st.button("Clear history"):
        st.session_state.history = []
        st.rerun()

st.title("🏠 India House Price Predictor")
st.caption("Multi-city model — Mumbai, Delhi, Bangalore, Chennai, Kolkata, Hyderabad")

col1, col2 = st.columns(2)
with col1:
    city = st.selectbox("City", cities)
    area = st.slider("Area (sqft)", 200, 10000, 1200)
    bedrooms = st.slider("Bedrooms", 1, 6, 2)
with col2:
    resale = st.radio("Resale property?", ["No", "Yes"], horizontal=True)
    gym = st.checkbox("Gymnasium")
    pool = st.checkbox("Swimming Pool")
    security = st.checkbox("24x7 Security")

if st.button("Predict Price", type="primary"):
    row = {f: 0 for f in feature_names}
    row["Area"] = area
    if "No. of Bedrooms" in row: row["No. of Bedrooms"] = bedrooms
    if "Resale" in row: row["Resale"] = 1 if resale == "Yes" else 0
    if "Gymnasium" in row: row["Gymnasium"] = 1 if gym else 0
    if "SwimmingPool" in row: row["SwimmingPool"] = 1 if pool else 0
    if "24X7Security" in row: row["24X7Security"] = 1 if security else 0
    city_col = f"City_{city}"
    if city_col in row: row[city_col] = 1

    input_df = pd.DataFrame([row])[feature_names]
    log_pred = model.predict(input_df)[0]
    price_pred = np.expm1(log_pred)

    st.success(f"### Estimated Price: ₹{price_pred:,.0f}")

    st.session_state.history.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "summary": f"{city}, {area}sqft → ₹{price_pred:,.0f}"
    })
else:
    st.info("Fill in the details and click Predict Price.")