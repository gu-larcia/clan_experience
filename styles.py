"""OSRS-themed CSS for Streamlit."""

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Crimson+Text:wght@400;600&display=swap');

:root {
    --gold: #d4af37;
    --gold-dark: #b8860b;
    --parchment: #f4e4bc;
    --parchment-dark: #e8d5a3;
    --wood: #8b7355;
    --wood-dark: #5c4d3a;
    --ocean: #1a2a3a;
    --active: #2ecc71;
    --at-risk: #f1c40f;
    --inactive: #e67e22;
    --churned: #e74c3c;
}

.stApp {
    background: linear-gradient(180deg, #0d1520 0%, #1a2a3a 50%, #0d1520 100%);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--parchment) 0%, var(--parchment-dark) 100%);
    border-right: 4px solid var(--wood);
}
[data-testid="stSidebar"] * {
    color: var(--wood-dark) !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-family: 'Cinzel', serif !important;
}

/* Headers */
.stApp h1, .stApp h2, .stApp h3 {
    font-family: 'Cinzel', serif !important;
    color: var(--gold) !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.6);
}
.stApp h1 {
    border-bottom: 3px solid var(--gold-dark);
    padding-bottom: 10px;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: linear-gradient(180deg, var(--wood) 0%, var(--wood-dark) 100%);
    border-radius: 8px 8px 0 0;
    padding: 5px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Cinzel', serif !important;
    color: var(--parchment) !important;
    background: transparent;
    border-radius: 6px 6px 0 0;
    padding: 10px 20px;
}
.stTabs [data-baseweb="tab"]:hover {
    background: rgba(255,215,0,0.2);
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(180deg, var(--gold-dark) 0%, #b8860b 100%) !important;
    color: var(--wood-dark) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: linear-gradient(180deg, rgba(244,228,188,0.08) 0%, rgba(244,228,188,0.03) 100%);
    border: 2px solid var(--wood);
    border-top: none;
    border-radius: 0 0 8px 8px;
    padding: 20px;
}

/* Metrics */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, var(--wood) 0%, var(--wood-dark) 100%);
    border: 2px solid var(--gold-dark);
    border-radius: 10px;
    padding: 15px;
}
[data-testid="stMetric"] label {
    font-family: 'Cinzel', serif !important;
    color: var(--gold) !important;
}
[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-family: 'Crimson Text', serif !important;
    color: var(--parchment) !important;
}

/* Buttons */
.stButton > button {
    font-family: 'Cinzel', serif !important;
    background: linear-gradient(180deg, var(--gold) 0%, var(--gold-dark) 100%);
    color: var(--wood-dark) !important;
    border: 2px solid #b8860b;
    border-radius: 6px;
    font-weight: 600;
}
.stButton > button:hover {
    background: linear-gradient(180deg, #ffec80 0%, var(--gold) 100%);
    transform: translateY(-1px);
}

/* Inputs */
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: var(--parchment) !important;
    border: 2px solid var(--wood) !important;
}

/* DataFrames */
[data-testid="stDataFrame"] {
    border: 3px solid var(--wood);
    border-radius: 8px;
}

/* Alerts */
.stAlert {
    font-family: 'Crimson Text', serif;
    border-radius: 6px;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: var(--wood-dark);
    border-radius: 4px;
}
::-webkit-scrollbar-thumb {
    background: var(--gold-dark);
    border-radius: 4px;
}
</style>
"""
