import streamlit as st
import pandas as pd
import numpy as np

df = pd.read_csv("premier_league_complete_stats_whole2025-2026_season_UPDATED.csv")

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
top_scorer = df.loc[df["goals"].idxmax()] # Find the player with the most goals
top_assister = df.loc[df["assists"].idxmax()] # Find the player with the most assists
top_rated = df.loc[df["rating"].idxmax()] # Find the player with the highest FotMob rating

with col1: # First column for top goalscorer
    st.metric(
        label="Top goalscorer",
        value=top_scorer["player_name"],
        delta=f"{int(top_scorer['goals'])} goals"
    ) # Display the top goalscorer with their name and number of goals

with col2: # Second column for top assister
    st.metric(
        label="Top assister", 
        value=top_assister["player_name"],
        delta=f"{int(top_assister['assists'])} assists" # Display the top assister with their name and number of assists
    ) # Display the top assister with their name and number of assists

with col3: # Third column for top rated player
    st.metric(
        label="Top FotMob rating",
        value=top_rated["player_name"],
        delta=f"{top_rated['rating']:.2f}" # Display the top rated player with their name and FotMob rating
    ) # Display the top rated player with their name and FotMob rating

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(["Premier League Player Statistics", "Premier League standings", "Tournament Snapshot", "Fan Introduction form"]) # Create tabs for different sections of the dashboard

with tab1: # First tab for Premier League Player Statistics
    st.subheader("Premier League Player Statistics") # Add a subheader for the first tab

    if "filters_active" not in st.session_state: # Check if the session state variable "filters_active" exists, and if not, initialize it to True
        st.session_state.filters_active = True # Initialize a session state variable to track whether filters are active

    # FILTERS
    col1, col2 = st.columns(2) # Create two columns for filters

    with col1: # First column for position filter
        positions = st.multiselect(
            "Filter by position",
            options=sorted(df["position"].dropna().unique()), # Get unique positions from the dataframe and sort them for the multiselect options
            default=sorted(df["position"].dropna().unique()) # Set the default selected positions to all unique positions in the dataframe
        ) # Create a multiselect filter for positions, allowing users to select multiple positions to filter the data

    with col2: # Second column for minimum rating filter
        min_rating = st.slider(
            "Minimum FotMob rating",
            min_value=0.0,
            max_value=float(df["rating"].max()), # Set the maximum value of the slider to the maximum rating in the dataframe
            value=0.0,
            step=0.1
        ) # Create a slider filter for minimum FotMob rating, allowing users to set a minimum rating threshold for the data

    # CLEAR FILTERS BUTTON

    if st.button("Clear filters"): # Create a button to clear the filters
        st.session_state.filters_active = False # Set the session state variable to False when the button is clicked
        st.rerun() # Rerun the app to reset the filters

    # APPLY FILTERS
    if min_rating == 0: # If the minimum rating is set to 0, filter the dataframe only by position
        filtered_df = df[
            df["position"].isin(positions) # Filter the dataframe to include only players whose position is in the selected positions
        ] # Filter the dataframe to include only players whose position is in the selected positions
    else:
        filtered_df = df[
            (df["position"].isin(positions)) & # Filter the dataframe to include only players whose position is in the selected positions and whose rating is not null and greater than or equal to the minimum rating
            (df["rating"].notna()) & # Filter the dataframe to include only players whose position is in the selected positions and whose rating is not null and greater than or equal to the minimum rating
            (df["rating"] >= min_rating) # Filter the dataframe to include only players whose position is in the selected positions and whose rating is not null and greater than or equal to the minimum rating
        ]

    # METRICS
    metric1, metric2, metric3 = st.columns(3) # Create three columns for metrics

    with metric1:
        st.metric(
            "Players shown",
            len(filtered_df) # Display the number of players shown in the filtered dataframe
        ) # Display the number of players shown in the filtered dataframe

    with metric2:
        st.metric(
            "Average rating",
            round(filtered_df["rating"].mean(), 2) # Display the average FotMob rating of the players shown in the filtered dataframe, rounded to two decimal places
        ) # Display the average FotMob rating of the players shown in the filtered dataframe, rounded to two decimal places

    with metric3:
        st.metric(
            "Total goals",
            int(filtered_df["goals"].sum()) # Display the total number of goals scored by the players shown in the filtered dataframe, converted to an integer
        ) # Display the total number of goals scored by the players shown in the filtered dataframe, converted to an integer

    st.divider()

    # TABLE
    st.subheader("Filtered Players") # Add a subheader for the filtered players table

    display_columns = [
        "player_name",
        "team_name",
        "position",
        "appearances",
        "goals",
        "assists",
        "rating"
    ] # Define the columns to display in the filtered players table

    st.dataframe(
        filtered_df[display_columns], # Display the filtered players table with the specified columns
        hide_index=True,
        use_container_width=True
    ) # Display the filtered players table with the specified columns, hiding the index and using the container width for better visibility

    # CHART 1
    st.subheader("Player Ratings")

    rating_chart = (
        filtered_df
        .sort_values("rating", ascending=False) # Sort the filtered dataframe by FotMob rating in descending order
        .head(10) # Select the top 10 players by FotMob rating
        .set_index("player_name")["rating"] # Set the player names as the index and select the FotMob rating column for the chart
    ) # Create a chart showing the top 10 players by FotMob rating, sorted in descending order and using the player names as the index

    st.bar_chart(rating_chart) # Display a bar chart of the top 10 players by FotMob rating, using the player names as the x-axis and the ratings as the y-axis

    # CHART 2
    st.subheader("Goals by Team")

    goals_by_team = (
        filtered_df
        .groupby("team_name")["goals"] #Group the filtered dataframe by team name and sum the goals scored by each team
        .sum() # Sum the goals for each team
        .sort_values(ascending=False) # Sort the teams by total goals in descending order
    ) # Create a chart showing the total goals scored by each team, sorted in descending order

    st.line_chart(goals_by_team) # Display a line chart of the total goals scored by each team, using the team names as the x-axis and the total goals as the y-axis


with tab2: # Second tab for Premier League standings
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

with tab3: # Third tab for Tournament Snapshot
    st.subheader("Tournament Snapshot")

    st.write(
        "Manchester United finished 3rd in the Premier League, "
        "qualifying for the UEFA Champions League. "
        "They were eliminated in the Round of 16 of the UEFA Champions League, "
        "and reached the semi-finals of the FA Cup."
    )

with tab4: # Fourth tab for Fan Introduction form

    # SESSION STATE

    if "name_error" not in st.session_state:
        st.session_state.name_error = False

    if "submissions" not in st.session_state:
        st.session_state.submissions = 0

    if "step" not in st.session_state:
        st.session_state.step = 1

    st.metric("Fan Introductions", st.session_state.submissions)

    st.caption(f"Step {st.session_state.step} of 4")


    # STEP 1: NAME

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


    # STEP 2: PLAYER + YEARS

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


    # STEP 3: LEAGUE + FORM

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


    # STEP 4: MANAGER + RECOMMEND

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


    # RESPONSES

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