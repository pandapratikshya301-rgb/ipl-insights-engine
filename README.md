# 🏏 IPL Insights Engine
**AI-Powered Predictive Analytics & Advanced Match Strategy**

An enterprise-grade, highly interactive cricket analytics dashboard built to visualize historical IPL data and predict match outcomes using Machine Learning and Generative Heuristics.

---

## 🌟 Key Features

### 🕵️ Advanced Player Scouting (Radar Engine)
Evaluates a batter's prowess dynamically across different match phases (Powerplay, Middle Overs, Death Overs) using multidimensional radar charts. Generates an AI scouting report to classify players as "Elite Finishers" or "Powerplay Specialists."

### 📉 The "Worm Chart" Time Machine
Step back in time to visualize the exact flow and momentum shifts of historical matches. Plots cumulative run rates and interactive Fall of Wickets markers across all 20 overs.

### 🧠 Machine Learning Match Predictor
Utilizes a **Random Forest Classifier** trained on historical team form, venue data, and toss decisions to output precise victory probabilities. Includes **Feature Importance** breakdown for model explainability.

### 🤖 GenAI Smart Narrative
Going beyond raw numbers, the engine digests the predictive probabilities, venue context, and toss decisions to auto-generate fluid, ESPN-style professional analysis paragraphs. 

### 🏟️ Venue Intelligence & Micro-Battles
Identify chasing vs. defending biases for specific stadiums and analyze deep Head-to-Head (Batter vs. Bowler) matchups to see exactly where games are won or lost.

---

## 🚀 Accessing the Dashboard

The application features a secure, cinematic gateway for evaluators. 
**Access Code:** `evaluator`

---

## 🛠️ Technology Stack
- **Frontend UI:** Streamlit (Custom Glassmorphism, Advanced CSS Styling)
- **Data Visualization:** Plotly Graph Objects & Plotly Express
- **Machine Learning:** Scikit-Learn (RandomForestClassifier)
- **Data Processing:** Pandas & NumPy

---

## 💻 Local Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ipl-insights-engine.git
   cd ipl-insights-engine
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run data/app.py
   ```
