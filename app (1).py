import streamlit as st
from player_scouting_utils import load_data, process_batter_stats, score_batters

st.set_page_config(page_title="AI-Powered Player Scouting", layout="wide")
st.title(" AI-Powered Player Scouting App")

st.markdown("Upload IPL data and scout top batters phase-wise using AI-style ranking.")

deliveries_file = st.file_uploader("Upload deliveries_till_2024.csv", type="csv")
matches_file = st.file_uploader("Upload matches_till_2024.csv", type="csv")

if deliveries_file and matches_file:
    df = load_data(deliveries_file, matches_file)
    scouting_df = process_batter_stats(df)

    st.success("Data processed successfully!")

    phase = st.selectbox("Select Phase", ["Powerplay", "Middle", "Death"])
    min_sr = st.slider("Minimum Strike Rate", 0, 200, 120)
    min_runs = st.slider("Minimum Runs", 0, 300, 50)
    w_sr = st.slider("Weight: Strike Rate", 0.0, 1.0, 0.6)
    w_runs = 1.0 - w_sr

    filtered = scouting_df[
        (scouting_df[f"strike_rate_{phase}"] >= min_sr) &
        (scouting_df[f"runs_{phase}"] >= min_runs)
    ]

    ranked = score_batters(filtered.copy(), phase, w_sr=w_sr, w_runs=w_runs)

    st.subheader(" AI-Ranked Batters")
    st.dataframe(ranked.reset_index(drop=True), use_container_width=True)
