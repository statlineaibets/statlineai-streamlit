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
        # Parse and organize the prop data
        props = props_data.get("included", [])
        rows = []

        for item in props:
            if item.get("type") == "new_player_stat":
                attributes = item["attributes"]
                player_name = attributes.get("name")
                stat_type = attributes.get("stat_type")
                line_score = attributes.get("line_score")
                team = attributes.get("team")
                opponent = attributes.get("opponent")

                rows.append({
                    "Player": player_name,
                    "Stat": stat_type,
                    "Line": line_score,
                    "Team": team,
                    "Opponent": opponent
                })

        if rows:
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No player props available.")
    except Exception as e:
        st.error(f"Error displaying props: {str(e)}")

