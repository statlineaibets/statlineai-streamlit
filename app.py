import streamlit as st
import requests
import pandas as pd

PRIZEPICKS_PROXY_URL = https://prizepicks-proxy-bahamm34za-uc.a.run.app

def get_live_props():
    try:
        response = requests.get(PRIZEPICKS_PROXY_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

st.set_page_config(page_title="StatlineAI Live Props", layout="wide")
st.title("StatlineAI | Live PrizePicks Props")

if st.button("Refresh Props"):
    st.rerun()

props_data = get_live_props()

if "error" in props_data:
    st.error(f"Failed to load data: {props_data['error']}")
else:
    try:
        props = props_data.get("data", [])
        rows = []

        for item in props:
            attributes = item.get("attributes", {})
            player_name = attributes.get("name", "N/A")
            stat_type = attributes.get("stat_type", "N/A")
            line_score = attributes.get("line_score", "N/A")
            team = attributes.get("team", "N/A")
            opponent = attributes.get("opponent", "N/A")

            rows.append({
                "Player": player_name,
                "Stat": stat_type,
                "Line": line_score,
                "Team": team,
                "Opponent": opponent
            })

        if rows:
            df = pd.DataFrame(rows)
            st.dataframe(df)
        else:
            st.warning("No player props available.")
    except Exception as e:
        st.error(f"Error parsing data: {e}")
