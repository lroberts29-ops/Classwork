import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Manchester United 2025/26 season stats", page_icon="\U0001F3C6", layout="wide")

RED = "#DA020E"
BLACK = "#000000"
CARD = "#407FE6"
INK = "#FBE122"

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

tab1, tab2, tab3, tab4 = st.tabs(["Average FotMob rating", "Premier League standings", "Tournament Snapshot", "Fan Introduction form"])

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

with tab4:

    # -------------------------
    # SESSION STATE
    # -------------------------

    if "name_error" not in st.session_state:
        st.session_state.name_error = False

    if "submissions" not in st.session_state:
        st.session_state.submissions = 0

    if "step" not in st.session_state:
        st.session_state.step = 1

    st.metric("Fan Introductions", st.session_state.submissions)

    st.caption(f"Step {st.session_state.step} of 4")


    # -------------------------
    # STEP 1: NAME
    # -------------------------

    if st.session_state.step == 1:

        st.text_input(
            "Your name",
            value=st.session_state.get("name", ""),
            key="name_field"
        )

        if st.session_state.name_error:
            st.error("Please enter your name before continuing.")

        if st.button("Next →"):

            if st.session_state.name_field.strip() == "":
                st.session_state.name_error = True
                st.rerun()

            else:
                st.session_state.name = st.session_state.name_field
                st.session_state.name_error = False
                st.session_state.step = 2
                st.rerun()


    # -------------------------
    # STEP 2: PLAYER + YEARS
    # -------------------------

    elif st.session_state.step == 2:

        player_name = st.selectbox(
            "Who is your favorite Manchester United player?",
            [
                "Bruno Fernandes",
                "Casemiro",
                "Mason Mount",
                "Kobbie Mainoo",
                "Amad Diallo",
                "Other"
            ]
        )

        years = st.slider(
            "How long have you been a Manchester United fan?",
            min_value=1,
            max_value=60,
            value=10
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("← Back"):
                st.session_state.step = 1
                st.rerun()

        with col2:
            if st.button("Next →"):
                st.session_state.player_name = player_name
                st.session_state.years = years
                st.session_state.step = 3
                st.rerun()


    # -------------------------
    # STEP 3: LEAGUE + FORM
    # -------------------------

    elif st.session_state.step == 3:

        league_position = st.number_input(
            "What position do you think Manchester United will finish in the Premier League this season?",
            min_value=1,
            max_value=20,
            value=10
        )

        current_form = st.radio(
            "How do you rate Manchester United's current form?",
            ["Poor", "Average", "Good", "Excellent"]
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("← Back"):
                st.session_state.step = 2
                st.rerun()

        with col2:
            if st.button("Next →"):
                st.session_state.league_position = league_position
                st.session_state.current_form = current_form
                st.session_state.step = 4
                st.rerun()


    # -------------------------
    # STEP 4: MANAGER + RECOMMEND
    # -------------------------

    elif st.session_state.step == 4:

        favorite_manager = st.selectbox(
            "Who is your favorite Manchester United manager?",
            [
                "Sir Matt Busby (1945-1969, 1970-1971)",
                "Wilf McGuinness (1969-1970)",
                "Frank O'Farrell (1971-1972)",
                "Tommy Docherty (1972-1977)",
                "Dave Sexton (1977-1981)",
                "Ron Atkinson (1981-1986)",
                "Sir Alex Ferguson (1986-2013)",
                "David Moyes (2013-2014)",
                "Ryan Giggs (2014, interim)",
                "Louis van Gaal (2014-2016)",
                "José Mourinho (2016-2018)",
                "Ole Gunnar Solskjær (2018-2021)",
                "Michael Carrick (2021, interim)",
                "Ralf Rangnick (2021-2022, interim)",
                "Erik ten Hag (2022-2024)",
                "Ruben Amorim (2024-2026)",
                "Michael Carrick (2026-present)"
            ]
        )

        would_recommend = st.checkbox(
            "Would you recommend this dashboard to other Manchester United fans?"
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("← Back"):
                st.session_state.step = 3
                st.rerun()

        with col2:
            if st.button("Submit →"):

                st.session_state.favorite_manager = favorite_manager
                st.session_state.would_recommend = would_recommend

                if "responses" not in st.session_state:
                    st.session_state.responses = []

                st.session_state.responses.append({
                    "name": st.session_state.name,
                    "player": st.session_state.player_name,
                    "years": st.session_state.years,
                    "league_position": st.session_state.league_position,
                    "current_form": st.session_state.current_form,
                    "favorite_manager": st.session_state.favorite_manager,
                    "would_recommend": st.session_state.would_recommend
                })

                st.session_state.submissions += 1

                st.success("Fan introduction submitted!")

                st.session_state.step = 1
                st.session_state.name_error = False

                st.rerun()


    # -------------------------
    # RESPONSES
    # -------------------------

    if st.session_state.get("responses"):

        st.subheader("Today's Fan Introductions")

        for i, r in enumerate(st.session_state.responses):

            st.write(
                f"**{r['name']}** — Favorite player: "
                f"**{r['player']}**, fan for **{r['years']} years**"
            )

            st.write(
                f"Predicted finish: **{r['league_position']}** | "
                f"Current form: **{r['current_form']}**"
            )

            st.write(
                f"Favorite manager: **{r['favorite_manager']}**"
            )

            if r["would_recommend"]:
                st.write("👍 Would recommend the dashboard")

            if st.button("Delete", key=f"del_{i}"):

                st.session_state.responses.pop(i)
                st.session_state.submissions -= 1
                st.rerun()

        if st.button("Clear All Responses"):

            st.session_state.responses = []
            st.session_state.submissions = 0
            st.rerun()