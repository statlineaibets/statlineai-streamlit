import streamlit as st
import requests
import pandas as pd

PRIZEPICKS_PROXY_URL = "https://prizepicks-proxy-731823355083.us-central1.run.app"

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
        props = props_data.get("included", [])
        rows = []

        for item in props:
            attributes = item.get("attributes", {})
            rows.append({
                "Player": attributes.get("name", "N/A"),
                "Stat": attributes.get("stat_type", "N/A"),
                "Line": attributes.get("line_score", "N/A"),
                "Team": attributes.get("team", "N/A"),
                "Opponent": attributes.get("opponent", "N/A"),
            })

        if rows:
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No player props available.")

    except Exception as e:
        st.error(f"Error parsing props: {str(e)}")
