import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Manchester United 2025/26 season stats", page_icon="\U0001F3C6", layout="wide")

RED = "#EC0303"
BLACK = "#050505"
CARD = "#142A4D"
INK = "#F2EDE4"

st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {RED};
        }}
        h1, h2, h3 {{
            font-family: Georgia, serif !important;
            color: {INK} !important;
        }}
        p, li, span, .stMarkdown, .stCaption, label {{
            color: {INK} !important;
        }}
        [data-testid="stMetricValue"] {{
            color: {BLACK} !important;
        }}
        [data-testid="stMetricLabel"] {{
            color: {INK} !important;
        }}
        section[data-testid="stSidebar"] {{
            background-color: {CARD};
        }}
        .stTabs [data-baseweb="tab"] {{
            color: {INK};
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Manchester United 2025/26 Season Stats — Dashboard")
st.caption("Real, verified football data. Built entirely with columns, tabs, sidebar, and an expander.")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Top goalscorer", value="Sesko", delta="11 goals")

with col2:
    st.metric(label="Top assister", value="B. Fernandes", delta="Record breaking: 21 assists")

with col3:
    st.metric(label="Top FotMob", value="B. Fernandes", delta="8.03")

st.divider()

tab1, tab2, tab3 = st.tabs(["Average FotMob rating", "Premier League standings", "Tournament Snapshot"])

with tab1:
    st.subheader("Top 5 Manchester United ratings")

    players = pd.DataFrame(
        {
            "Player": ["B. Fernandes", "Casemiro", "Cunha", "Mbeumo", "Diallo"],
            "Position": ["Midfielder", "Midfielder", "Forward", "Forward", "Forward"],
            "Rating": [8.03, 7.33, 7.29, 7.19, 7.19],
        }
    )

    if st.checkbox('Show in-depth stats'):
        players_names=['B. Fernandes', 'Casemiro', 'Cunha', 'Mbeumo', 'Diallo']
        players_data = pd.DataFrame({
            'Appearances': [37, 35, 36, 34, 33],
            'Minutes': [3203, 2600, 2683, 2670, 2428],
            'Goals': [9, 9, 10, 12, 2]
        },
            columns=['Appearances', 'Minutes', 'Goals'],
            index = players_names
        )
        players_data

    chart_col, table_col = st.columns([2, 1])

    with chart_col:
        st.bar_chart(players.set_index("Player")["Rating"])

    with table_col:
        st.dataframe(players, hide_index=True, use_container_width=True)

    st.caption(
        "B. Fernandes breaks the record for the most assists in a single season with 21 earning him the top FotMob rating of 8.03 in the Premier League"
    )

with tab2:
    st.subheader("How the League Finished")

    podium = pd.DataFrame(
        {
            "Place": [1, 2, 3, 4],
            "Team": ["Arsenal", "Manchester City", "Manchester United", "Aston Villa"],
            "Result": [
                "Champion",
                "Runner-up",
                "3rd",
                "4th",
            ],
        }
    )
    st.dataframe(podium, hide_index=True, use_container_width=True)
