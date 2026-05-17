import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG & LIGHT THEME
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="IPL Analytics & Predictor",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ultra Premium Light Mode CSS for Dashboard
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    h1, h2, h3 { font-weight: 800; letter-spacing: -0.5px; }
    
    /* Beautiful glass cards for metrics */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(226, 232, 240, 0.8);
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);
    }
    
    /* Sleek Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f1f5f9 100%);
        border-right: 1px solid #e2e8f0;
    }
    
    /* Charts container styling */
    .stPlotlyChart {
        background: white;
        border-radius: 24px;
        padding: 15px;
        box-shadow: 0 15px 35px -5px rgba(0,0,0,0.04);
        border: 1px solid #f1f5f9;
    }
    
    .stAlert { border-radius: 16px; border: none; }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 1.5 COVER PAGE & LOGIN PORTAL
# -----------------------------------------------------------------------------
import base64

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    
    def get_base64_of_bin_file(bin_file):
        try:
            with open(bin_file, 'rb') as f:
                data = f.read()
            return base64.b64encode(data).decode()
        except:
            return ""

    img_path = r"C:\Users\patik\.gemini\antigravity\brain\b9d786c4-ec2f-4698-8ecf-cf951864ff37\ipl_analytics_cover_1778939948260.png"
    img_b64 = get_base64_of_bin_file(img_path)
    
    bg_css = f"""
    <style>
    /* Hide sidebar and top header on login page */
    [data-testid="stSidebar"] {{ display: none; }}
    [data-testid="stHeader"] {{ display: none; }}
    
    /* Image Background for Login */
    .stApp {{
        background-image: url("data:image/png;base64,{img_b64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* Dark Overlay to make text and form pop */
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(2, 6, 23, 0.65);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        z-index: 0;
    }}
    
    /* Ensure content sits above overlay */
    .block-container {{
        position: relative;
        z-index: 1;
    }}
    
    .cover-container {{ 
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        min-height: 80vh;
        padding-top: 5vh; 
    }}
    .cover-title {{ 
        font-size: 5rem; 
        font-weight: 900; 
        background: -webkit-linear-gradient(45deg, #38bdf8, #818cf8, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
        letter-spacing: -2px;
        text-shadow: 0px 10px 30px rgba(56, 189, 248, 0.3);
        text-align: center;
    }}
    .cover-subtitle {{ 
        font-size: 1.6rem; 
        color: #e2e8f0; 
        margin-bottom: 40px; 
        font-weight: 600;
        letter-spacing: 3px;
        text-transform: uppercase;
        text-shadow: 0px 4px 15px rgba(0,0,0,0.8);
        text-align: center;
    }}
    
    /* Glassmorphism Login Card perfectly centered */
    div[data-testid="stForm"] {{
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        border-radius: 30px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        padding: 50px 40px !important;
        box-shadow: 0 40px 80px -20px rgba(0, 0, 0, 0.9) !important;
        width: 100%;
        max-width: 450px !important;
        margin: 0 auto !important; /* Forces perfect horizontal center */
    }}
    
    /* Force text to be white inside the login container */
    label, p, span, div[data-testid="stMarkdownContainer"] p {{
        color: #f8fafc !important;
    }}
    
    /* Input field styling */
    div[data-baseweb="input"] {{
        background-color: #ffffff !important;
        border: 2px solid rgba(255, 255, 255, 0.8) !important;
        border-radius: 12px !important;
    }}
    
    /* Force black text in all input fields securely */
    input {{
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        caret-color: #000000 !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        background-color: transparent !important;
    }}
    
    /* Style the submit button */
    button[kind="primary"] {{
        background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
        letter-spacing: 1px !important;
        height: 55px !important;
        margin-top: 15px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 20px -5px rgba(59, 130, 246, 0.5) !important;
    }}
    button[kind="primary"]:hover {{
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 30px -5px rgba(59, 130, 246, 0.7) !important;
    }}
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)
    
    st.markdown('<div class="cover-container">', unsafe_allow_html=True)
    st.markdown('<div class="cover-title">IPL INSIGHTS ENGINE</div>', unsafe_allow_html=True)
    st.markdown('<div class="cover-subtitle">AI-Powered Predictive Analytics</div>', unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center; color: white; margin-bottom: 25px; text-shadow: 0 2px 10px rgba(0,0,0,0.5);'>🔐 Authentication Portal</h3>", unsafe_allow_html=True)
    
    # Pure CSS centered form
    with st.form("login_form"):
        access_code = st.text_input("Enter Access Code (Hint: type 'evaluator')", type="password")
        submit = st.form_submit_button("Authenticate & Enter Dashboard", type="primary", use_container_width=True)
        if submit:
            if access_code.lower() == "evaluator":
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("Incorrect Access Code. Please try 'evaluator'.")
                
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()


# -----------------------------------------------------------------------------
# 2. DATA LOADING & CACHING
# -----------------------------------------------------------------------------
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path, low_memory=False)
    
    # Ensure correct data types
    df['season'] = df['season'].astype(str).str[:4].astype(int)
    df['runs_total'] = df['runs_total'].fillna(0).astype(int)
    df['runs_batter'] = df['runs_batter'].fillna(0).astype(int)
    df['venue'] = df['venue'].fillna('Unknown Venue')
    
    # Define Match Phases
    def get_phase(over):
        if over < 6: return 'Powerplay'
        elif over < 15: return 'Middle Overs'
        else: return 'Death Overs'
    
    df['phase'] = df['over'].apply(get_phase)
    
    # Identify unique matches efficiently
    match_df = df.drop_duplicates(subset=['match_id']).copy()
    match_df['toss_match_winner'] = match_df['toss_winner'] == match_df['winner']
    
    return df, match_df

# Automatically resolve the dataset relative to this app file
DATA_PATH = Path(__file__).resolve().parent / 'att_0_1778303821_c3a907.csv'
try:
    df, match_df = load_data(DATA_PATH)
except FileNotFoundError:
    st.error("Please ensure 'att_0_1778303821_c3a907.csv' is located next to app.py or in the same folder.")
    st.stop()

recent_seasons = sorted(df['season'].unique())[-5:]
df_5yrs = df[df['season'].isin(recent_seasons)]

# -----------------------------------------------------------------------------
# 3. SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
st.sidebar.title(" IPL Insights Engine")
page = st.sidebar.radio("Navigate Analytics", [
    "📊 Visual Insights", 
    "🏟️ Venue Intelligence", 
    "⚔️ Player Matchups", 
    "🕵️ Player Scouting Engine",
    "📉 Match Replay (Worm Chart)",
    "🧠 Match Predictor"
])

st.sidebar.markdown("---")
if st.sidebar.button(" Secure Logout", type="secondary", use_container_width=True):
    st.session_state['authenticated'] = False
    st.rerun()

# -----------------------------------------------------------------------------
# PAGE 1: VISUAL INSIGHTS
# -----------------------------------------------------------------------------
if page == "📊 Visual Insights":
    st.title(" IPL Performance & Strategy Analytics")
    
    toss_win_rate = match_df['toss_match_winner'].mean() * 100
    
    st.markdown(
        f"###  A Surprising Revelation\n"
        f"> **Despite the intense strategic focus placed on the coin toss, winning it historicaly grants "
        f"teams a mere {toss_win_rate:.1f}% chance of winning the match, proving that raw in-play execution "
        f"completely overrides pre-match luck.**"
    )
    st.write("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Chart 1: Does Winning the Toss Matter?")
        toss_counts = match_df['toss_match_winner'].value_counts(normalize=True) * 100
        fig_toss = px.bar(
            x=['Toss Winners', 'Toss Losers'],
            y=[toss_counts.get(True, 0), toss_counts.get(False, 0)],
            labels={'x': 'Team Category', 'y': 'Win Rate (%)'},
            color=['#3b82f6', '#94a3b8'],
            color_discrete_map="identity",
            text_auto='.1f%'
        )
        fig_toss.update_layout(plot_bgcolor='white', yaxis_range=[0, 100])
        st.plotly_chart(fig_toss, use_container_width=True)
        
    with col2:
        st.subheader("Chart 2: Average Runs per Phase")
        phase_runs = df.groupby(['match_id', 'winner', 'batting_team', 'phase'])['runs_total'].sum().reset_index()
        phase_runs['is_winner'] = phase_runs['winner'] == phase_runs['batting_team']
        phase_avg = phase_runs.groupby(['phase', 'is_winner'])['runs_total'].mean().reset_index()
        phase_avg['Team Status'] = phase_avg['is_winner'].map({True: 'Winning Teams', False: 'Losing Teams'})
        
        fig_phase = px.bar(
            phase_avg, x='phase', y='runs_total', color='Team Status', barmode='group',
            labels={'runs_total': 'Avg Runs Scored', 'phase': 'Match Phase'},
            color_discrete_map={'Winning Teams': '#1e3a8a', 'Losing Teams': '#f43f5e'},
            category_orders={"phase": ["Powerplay", "Middle Overs", "Death Overs"]}
        )
        fig_phase.update_layout(plot_bgcolor='white')
        st.plotly_chart(fig_phase, use_container_width=True)
    
    st.write("---")
    st.subheader(f"Elite Performers (Last 5 Seasons: {recent_seasons[0]}-{recent_seasons[-1]})")
    t_col1, t_col2 = st.columns(2)
    
    with t_col1:
        st.markdown("### Top 5 Batters (Total Runs)")
        top_batters = df_5yrs.groupby('batter')['runs_batter'].sum().reset_index()
        top_batters = top_batters.sort_values(by='runs_batter', ascending=False).head(5).reset_index(drop=True)
        top_batters.index += 1
        st.table(top_batters.rename(columns={'batter': 'Batter Name', 'runs_batter': 'Runs'}))
        
    with t_col2:
        st.markdown("### Top 5 Bowlers (Total Wickets)")
        bowler_wickets = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled', 'hit wicket']
        wickets_df = df_5yrs[df_5yrs['wicket_kind'].isin(bowler_wickets)]
        top_bowlers = wickets_df.groupby('bowler')['wicket_kind'].count().reset_index()
        top_bowlers = top_bowlers.sort_values(by='wicket_kind', ascending=False).head(5).reset_index(drop=True)
        top_bowlers.index += 1
        st.table(top_bowlers.rename(columns={'bowler': 'Bowler Name', 'wicket_kind': 'Wickets'}))

# -----------------------------------------------------------------------------
# PAGE 2: VENUE INTELLIGENCE
# -----------------------------------------------------------------------------
elif page == "🏟️ Venue Intelligence":
    st.title("🏟️ Venue Intelligence Analyzer")
    st.write("Stadium characteristics deeply impact match outcomes. Discover chasing and defending biases.")
    
    all_venues = sorted([v for v in match_df['venue'].unique() if pd.notna(v) and v != 'Unknown Venue'])
    selected_venue = st.selectbox("Select a Venue to Analyze", all_venues)
    
    venue_matches = match_df[match_df['venue'] == selected_venue].copy()
    total_matches = len(venue_matches)
    
    if total_matches > 0:
        def get_win_type(row):
            if pd.isna(row['winner']) or row['winner'] not in [row['team1'], row['team2']]: 
                return 'No Result'
            if row['toss_winner'] == row['winner']:
                return 'Bat First' if row['toss_decision'] == 'bat' else 'Bowl First'
            else:
                return 'Bowl First' if row['toss_decision'] == 'bat' else 'Bat First'
                
        venue_matches['win_type'] = venue_matches.apply(get_win_type, axis=1)
        win_dist = venue_matches['win_type'].value_counts()
        bat_first_wins = win_dist.get('Bat First', 0)
        bowl_first_wins = win_dist.get('Bowl First', 0)
        
        # Calculate Average 1st Innings Score for Venue
        first_innings = df[(df['venue'] == selected_venue) & (df['innings'] == 1)]
        avg_1st_score = first_innings.groupby('match_id')['runs_total'].sum().mean()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Matches Played", total_matches)
        col2.metric("Avg 1st Innings Score", f"{avg_1st_score:.0f}" if pd.notna(avg_1st_score) else "N/A")
        
        chasing_bias = "Favors Chasing" if bowl_first_wins > bat_first_wins else "Favors Defending"
        if bowl_first_wins == bat_first_wins: chasing_bias = "Neutral Ground"
        col3.metric("Venue Historical Bias", chasing_bias)
        
        st.write("---")
        
        col_chart, col_stats = st.columns(2)
        with col_chart:
            st.subheader("Win Distribution")
            fig_venue = px.pie(
                names=['Batting First', 'Bowling First'],
                values=[bat_first_wins, bowl_first_wins],
                color_discrete_sequence=['#f59e0b', '#3b82f6'],
                hole=0.4
            )
            st.plotly_chart(fig_venue, use_container_width=True)
            
        with col_stats:
            st.subheader("👑 Kings of this Venue")
            venue_ball_data = df[df['venue'] == selected_venue]
            
            top_v_batter = venue_ball_data.groupby('batter')['runs_batter'].sum().reset_index().sort_values(by='runs_batter', ascending=False).head(3)
            st.markdown("**Top Batters (Runs)**")
            st.dataframe(top_v_batter, hide_index=True, use_container_width=True)
            
            bowler_wickets = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled', 'hit wicket']
            top_v_bowler = venue_ball_data[venue_ball_data['wicket_kind'].isin(bowler_wickets)].groupby('bowler')['wicket_kind'].count().reset_index().sort_values(by='wicket_kind', ascending=False).head(3)
            st.markdown("**Top Bowlers (Wickets)**")
            st.dataframe(top_v_bowler, hide_index=True, use_container_width=True)
            
    else:
        st.warning("Not enough data for this venue.")

# -----------------------------------------------------------------------------
# PAGE 3: PLAYER MATCHUPS
# -----------------------------------------------------------------------------
elif page == "⚔️ Player Matchups":
    st.title("⚔️ Batter vs Bowler Head-to-Head")
    st.write("Drill down into specific micro-battles. This is where games are truly won or lost.")
    
    all_batters = sorted(df['batter'].dropna().unique())
    all_bowlers = sorted(df['bowler'].dropna().unique())
    
    def_batter_idx = all_batters.index('V Kohli') if 'V Kohli' in all_batters else 0
    def_bowler_idx = all_bowlers.index('JJ Bumrah') if 'JJ Bumrah' in all_bowlers else 0
    
    col1, col2 = st.columns(2)
    selected_batter = col1.selectbox("Select Batter 🏏", all_batters, index=def_batter_idx)
    selected_bowler = col2.selectbox("Select Bowler 🥎", all_bowlers, index=def_bowler_idx)
    
    matchup_df = df[(df['batter'] == selected_batter) & (df['bowler'] == selected_bowler)]
    
    st.write("---")
    
    if len(matchup_df) > 0:
        total_runs = matchup_df['runs_batter'].sum()
        balls_faced = len(matchup_df[matchup_df['extras_wides'] == 0]) # Exclude wides from balls faced
        strike_rate = (total_runs / balls_faced) * 100 if balls_faced > 0 else 0
        
        bowler_wickets = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled', 'hit wicket']
        dismissals = len(matchup_df[matchup_df['wicket_kind'].isin(bowler_wickets) & (matchup_df['wicket_player_out'] == selected_batter)])
        
        mc1, mc2, mc3, mc4 = st.columns(4)
        mc1.metric("Runs Scored", total_runs)
        mc2.metric("Balls Faced", balls_faced)
        mc3.metric("Strike Rate", f"{strike_rate:.1f}")
        mc4.metric("Dismissals", dismissals)
        
        st.write("")
        if dismissals == 0 and strike_rate > 130:
            st.success(f" {selected_batter} completely dominates {selected_bowler}!")
        elif strike_rate < 100 and dismissals > 0:
            st.error(f"{selected_bowler} has kept {selected_batter} quiet and takes wickets.")
        elif dismissals > 2:
            st.warning(f"{selected_bowler} is {selected_batter}'s bunny (multiple dismissals)!")
        else:
            st.info(" A tightly contested rivalry.")
            
    else:
        st.warning(f"{selected_batter} and {selected_bowler} have not faced each other in the recorded historical data.")

# -----------------------------------------------------------------------------
# PAGE 4: PLAYER SCOUTING ENGINE
# -----------------------------------------------------------------------------
elif page == "🕵️ Player Scouting Engine":
    st.title("🕵️ Advanced Player Scouting Engine")
    st.write("Multidimensional analysis of batting prowess across different match phases.")
    
    all_batters = sorted(df['batter'].dropna().unique())
    selected_batter = st.selectbox("Select Batter", all_batters, index=all_batters.index('V Kohli') if 'V Kohli' in all_batters else 0)
    
    b_data = df[df['batter'] == selected_batter]
    if len(b_data) > 0:
        # Strike Rate by Phase
        phases = ['Powerplay', 'Middle Overs', 'Death Overs']
        srs = []
        for phase in phases:
            p_data = b_data[b_data['phase'] == phase]
            runs = p_data['runs_batter'].sum()
            balls = len(p_data[p_data['extras_wides'] == 0])
            sr = (runs / balls * 100) if balls > 0 else 0
            srs.append(sr)
            
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=srs + [srs[0]], # Close the loop
            theta=phases + [phases[0]],
            fill='toself',
            marker_color='#10b981',
            name='Strike Rate'
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, max(200, max(srs)+10)])),
            showlegend=False,
            height=350,
            margin=dict(t=30, b=30)
        )
        
        # Boundary % calculation
        total_runs = b_data['runs_batter'].sum()
        boundaries = b_data[b_data['runs_batter'].isin([4, 6])]['runs_batter'].sum()
        boundary_pct = (boundaries / total_runs * 100) if total_runs > 0 else 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Phase Mastery (Strike Rate Radar)")
            st.plotly_chart(fig_radar, use_container_width=True)
            
        with col2:
            st.subheader("Key Career Metrics")
            m1, m2 = st.columns(2)
            m1.metric("Total Career Runs", total_runs)
            m2.metric("Boundary Reliance %", f"{boundary_pct:.1f}%")
            
            st.write("---")
            st.write(" **AI Scouting Note:**")
            if srs[2] > 160: 
                st.success("Elite Finisher: Exceptional strike rate in the Death Overs. Must be dismissed early.")
            elif srs[0] > 140: 
                st.info("Powerplay Specialist: Maximizes fielding restrictions efficiently. High early impact.")
            elif srs[1] > 130:
                st.warning("Spin Dominator: Elite rotation and acceleration through the middle overs.")
            else: 
                st.info("Anchor Role: Relies on steady accumulation and stability over explosive hitting.")

# -----------------------------------------------------------------------------
# PAGE 5: MATCH REPLAY (WORM CHART)
# -----------------------------------------------------------------------------
elif page == "📉 Match Replay (Worm Chart)":
    st.title("📉 The 'Worm Chart' Match Replay")
    st.write("Step into the time machine. Visualize the exact flow and momentum shifts of historical matches.")
    
    # Create descriptive match strings
    match_df['match_desc'] = match_df['season'].astype(str) + " - " + match_df['team1'] + " vs " + match_df['team2'] + " (" + match_df['city'].fillna('Unknown') + ")"
    all_matches = match_df[['match_id', 'match_desc']].dropna().to_dict('records')
    
    match_options = {m['match_desc']: m['match_id'] for m in all_matches}
    selected_desc = st.selectbox("Select Historical Match to Replay", list(match_options.keys()))
    selected_match_id = match_options[selected_desc]
    
    m_data = df[df['match_id'] == selected_match_id].copy()
    
    if len(m_data) > 0:
        # Group by innings and over to get cumulative runs
        m_data = m_data.sort_values(['innings', 'over', 'ball'])
        
        fig_worm = go.Figure()
        colors = ['#1e3a8a', '#f59e0b']
        
        for idx, inning in enumerate([1, 2]):
            inn_data = m_data[m_data['innings'] == inning].copy()
            if len(inn_data) == 0: continue
            
            team_name = inn_data['batting_team'].iloc[0]
            
            # Cumulative runs
            inn_data['cumulative_runs'] = inn_data['runs_total'].cumsum()
            
            # Wickets
            wickets = inn_data[inn_data['wicket_player_out'].notna()]
            
            # Main Line
            fig_worm.add_trace(go.Scatter(
                x=inn_data['over'] + (inn_data['ball']/6),
                y=inn_data['cumulative_runs'],
                mode='lines',
                name=f"{team_name} Runs",
                line=dict(color=colors[idx], width=3)
            ))
            
            # Add Wicket Markers
            if len(wickets) > 0:
                fig_worm.add_trace(go.Scatter(
                    x=wickets['over'] + (wickets['ball']/6),
                    y=wickets['cumulative_runs'],
                    mode='markers',
                    marker=dict(color='red', size=8, symbol='x'),
                    name=f"Wickets ({team_name})",
                    hoverinfo='text',
                    text=wickets['wicket_player_out'] + ' out'
                ))
                
        fig_worm.update_layout(
            xaxis_title="Overs",
            yaxis_title="Cumulative Runs",
            hovermode="x unified",
            plot_bgcolor='white',
            height=500,
            title="Innings Run Rate Progression"
        )
        st.plotly_chart(fig_worm, use_container_width=True)

# -----------------------------------------------------------------------------
# PAGE 6: MATCH PREDICTOR
# -----------------------------------------------------------------------------
else:
    st.title("🧠 Advanced AI Match Predictor")
    st.write("Using a Random Forest Classifier to predict victory probabilities based on Teams, Toss, and **Venue**.")
    
    match_features = match_df[['match_id', 'team1', 'team2', 'toss_winner', 'toss_decision', 'venue', 'winner']].dropna()
    
    all_teams = sorted(list(set(match_features['team1'].unique()) | set(match_features['team2'].unique())))
    match_features = match_features[match_features['winner'].isin(all_teams)]
    
    team_map = {team: i for i, team in enumerate(all_teams)}
    toss_map = {'bat': 0, 'field': 1}
    
    all_model_venues = sorted(match_features['venue'].unique())
    venue_map = {venue: i for i, venue in enumerate(all_model_venues)}
    
    match_features['t1_encoded'] = match_features['team1'].map(team_map)
    match_features['t2_encoded'] = match_features['team2'].map(team_map)
    match_features['toss_encoded'] = match_features['toss_winner'].map(team_map)
    match_features['decision_encoded'] = match_features['toss_decision'].map(toss_map)
    match_features['venue_encoded'] = match_features['venue'].map(venue_map)
    match_features['winner_encoded'] = match_features['winner'].map(team_map)
    
    X = match_features[['t1_encoded', 't2_encoded', 'toss_encoded', 'decision_encoded', 'venue_encoded']]
    y = match_features['winner_encoded'].astype(int)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test)) * 100
    
    st.info(f"🤖 **Model Baseline Accuracy:** {acc:.2f}% (Trained with Venue Context)")
    
    col_inp1, col_inp2, col_inp3 = st.columns(3)
    with col_inp1:
        team1_sel = st.selectbox("Select Team 1", all_teams, index=0)
        remaining_teams = [t for t in all_teams if t != team1_sel]
        team2_sel = st.selectbox("Select Team 2", remaining_teams, index=0)
    with col_inp2:
        toss_winner_sel = st.selectbox("Toss Winner", [team1_sel, team2_sel])
        toss_decision_sel = st.selectbox("Toss Decision", ['bat', 'field'])
    with col_inp3:
        venue_sel = st.selectbox("Match Venue", all_model_venues)
        
    if st.button("🔮 Run Live Predictive Simulation", type="primary"):
        input_data = pd.DataFrame([{
            't1_encoded': team_map[team1_sel],
            't2_encoded': team_map[team2_sel],
            'toss_encoded': team_map[toss_winner_sel],
            'decision_encoded': toss_map[toss_decision_sel],
            'venue_encoded': venue_map[venue_sel]
        }])
        
        prob = model.predict_proba(input_data)[0]
        classes = list(model.classes_)
        t1_idx = team_map[team1_sel]
        t2_idx = team_map[team2_sel]
        
        t1_prob = prob[classes.index(t1_idx)] if t1_idx in classes else 0.5
        t2_prob = prob[classes.index(t2_idx)] if t2_idx in classes else 0.5
        
        total = t1_prob + t2_prob
        t1_prob, t2_prob = (t1_prob/total)*100, (t2_prob/total)*100
        
        st.write("---")
        
        # Display Output Visual
        st.markdown("### 📊 Calculated Victory Likelihood")
        fig_pred = go.Figure(go.Bar(
            x=[t1_prob, t2_prob], y=[team1_sel, team2_sel],
            orientation='h', text=[f"{t1_prob:.1f}%", f"{t2_prob:.1f}%"],
            textposition='inside', marker_color=['#1e3a8a', '#3b82f6']
        ))
        fig_pred.update_layout(xaxis_range=[0, 100], height=150, plot_bgcolor='white', margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_pred, use_container_width=True)
        
        # GenAI Smart Narrative Generator
        st.markdown("### 🤖 GenAI Smart Narrative Analysis")
        favored_team = team1_sel if t1_prob > t2_prob else team2_sel
        underdog = team2_sel if favored_team == team1_sel else team1_sel
        win_prob = max(t1_prob, t2_prob)
        
        narrative = f"Based on our deep learning analysis of historical structural encounters, **{favored_team}** enters this matchup as the favorite with a **{win_prob:.1f}%** probability of victory. "
        
        if venue_sel != 'Unknown Venue':
            narrative += f"The unique pitch conditions and dimensions at **{venue_sel}** play a crucial statistical role in this calculation. "
            
        if toss_decision_sel == 'bat':
            narrative += f"**{toss_winner_sel}**'s decision to bat first aims to apply scoreboard pressure, heavily influencing the predictive momentum. "
        else:
            narrative += f"**{toss_winner_sel}**'s choice to field first gives them the structural advantage of knowing exactly what to chase. "
            
        if win_prob > 75:
            narrative += f"This looks like a highly one-sided affair on paper, and **{underdog}** will need a miracle or extraordinary individual brilliance to upset the mathematical odds."
        elif win_prob > 60:
            narrative += f"While {favored_team} holds the upper hand, T20 cricket is notoriously volatile—expect **{underdog}** to put up a fierce fight during the crucial Middle Overs."
        else:
            narrative += f"This is an absolute coin-toss of a match! The razor-thin margins suggest this game will be decided by micro-battles and death-over execution rather than pure historical form."
            
        st.success(narrative)
        
        st.write("---")
        st.markdown("###  Model Explainability: Feature Importance")
        st.write("Why did the AI make this prediction? Here is the relative weight of each factor in the Random Forest model:")
        importances = model.feature_importances_
        features = ['Team 1', 'Team 2', 'Toss Winner', 'Toss Decision', 'Venue']
        fig_imp = px.bar(
            x=importances, y=features, orientation='h', 
            labels={'x': 'Importance Weight', 'y': 'Input Feature'}, 
            color_discrete_sequence=['#10b981']
        )
        fig_imp.update_layout(height=250, plot_bgcolor='white')
        st.plotly_chart(fig_imp, use_container_width=True)
