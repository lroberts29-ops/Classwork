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

with st.form("Fan Introduction Form"):
    name = st.text_input("Who is your favorite Manchester United player?")
    st.write(f"{name}, is a great player!")

    league_position = st.number_input(
        "What position do you think Manchester United will finish in the Premier League this season?", 
        min_value=0, max_value=20, value=10
    )

    years = st.slider(
    "How long have you been a Manchester United fan?",
    min_value=1, max_value=60, value=30,
    )

    favorite_manager = st.selectbox(
    "Who is your favorite Manchester United manager?",
    ["Sir Matt Busby (1945-1969, 1970-1971)", "Wilf McGuiness (1969-1970)", "Frank O'Farrell (1971-1972)", "Tommy Docherty (1972-1977)", "Dave Sexton (1977-1981)", "Ron Atkinson (1981-1986)", "Sir Alex Ferguson (1986-2013)", "David Moyes (2013-2014)", "Ryan Giggs (2014, interim)", "Louis van Gaal (2014-2016)", "José Mourinho (2016-2018)", "Ole Gunnar Solskjær (2018-2021)", "Michael Carrick (2021, interim)", "Ralf Rangnick (2021-2022, interim)", "Erik ten Hag (2022-2024)", "Ruben Amorim (2024-2026)", "Michael Carrick (2026-present)"],
    )

    current_form = st.radio(
    "How do you rate Manchester United's current form?",
    ["Poor", "Average", "Good", "Excellent"],
    )

    would_recommend = st.checkbox(
    "Would you recommend this dashboard to other Manchester United fans?"
    )

    submitted =st.form_submit_button("Submit")

if submitted:
    st.divider()
    who = name if name else "An anonymous student"
    st.write(
        f"**{who}** spent **{minutes} min** in **{lot}** "
        f"during the **{time}**, frustration **{frustration}/10**."
    )
    if would_recommend:
        st.success("Thanks for recommending this dashboard to other Manchester United fans!")

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
