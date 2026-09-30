import streamlit as st
import pandas as pd

from data_loader import (
    load_infrastructure,
    load_cyclone
)

from risk_engine import calculate_risk


st.set_page_config(
    page_title="CycloneShield AI",
    page_icon="🌪️",
    layout="wide"
)


st.title("🌪️ CycloneShield AI")

st.subheader(
    "AI-Powered Cyclone Impact & Infrastructure Vulnerability Forecasting"
)


# Load data
infrastructure = load_infrastructure()
cyclone = load_cyclone().iloc[0]


st.sidebar.header("Cyclone Information")

st.sidebar.metric(
    "Wind Speed",
    f"{cyclone['wind_speed']} km/h"
)

st.sidebar.metric(
    "Rainfall",
    f"{cyclone['rainfall']} mm"
)

st.sidebar.metric(
    "Impact Radius",
    f"{cyclone['radius']} km"
)


# Calculate risk
results = []

for _, asset in infrastructure.iterrows():

    distance, score, level = calculate_risk(
        asset,
        cyclone
    )

    results.append({
        "Asset": asset["name"],
        "Type": asset["type"],
        "Distance (km)": round(distance, 2),
        "Risk Score": score,
        "Risk Level": level,
        "Criticality": asset["criticality"],
        "Latitude": asset["latitude"],
        "Longitude": asset["longitude"]
    })


results_df = pd.DataFrame(results)


# Sort by risk
results_df = results_df.sort_values(
    "Risk Score",
    ascending=False
)


# Metrics
col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Infrastructure",
    len(results_df)
)

col2.metric(
    "Critical",
    len(
        results_df[
            results_df["Risk Level"] == "CRITICAL"
        ]
    )
)

col3.metric(
    "High Risk",
    len(
        results_df[
            results_df["Risk Level"] == "HIGH"
        ]
    )
)

col4.metric(
    "Average Risk",
    round(results_df["Risk Score"].mean(), 1)
)


st.divider()


# Risk table
st.subheader("🚨 Infrastructure Risk Assessment")

st.dataframe(
    results_df[
        [
            "Asset",
            "Type",
            "Distance (km)",
            "Risk Score",
            "Risk Level"
        ]
    ],
    use_container_width=True
)


# Map
st.subheader("🗺️ Infrastructure Vulnerability Map")

map_data = results_df[
    [
        "Latitude",
        "Longitude"
    ]
]

st.map(
    map_data,
    latitude="Latitude",
    longitude="Longitude"
)


# Priority assets
st.subheader("🔥 Highest Priority Infrastructure")

top_assets = results_df.head(5)

for _, row in top_assets.iterrows():

    st.write(
        f"**{row['Asset']}** — "
        f"{row['Risk Level']} "
        f"({row['Risk Score']}/100)"
    )