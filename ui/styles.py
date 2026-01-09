"""OSRS-themed CSS for Streamlit."""

OSRS_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=MedievalSharp&display=swap');

:root {
    --parchment: #f4e4bc;
    --parchment-dark: #e8d5a3;
    --parchment-light: #faf3e0;
    --driftwood: #8b7355;
    --driftwood-dark: #5c4d3a;
    --driftwood-light: #a08b6d;
    --gold: #ffd700;
    --gold-dark: #d4af37;
    --gold-light: #ffec80;
    --ocean-dark: #1a2a3a;
    --ocean: #2d4a5a;
    --ocean-light: #3d6a7a;
    --status-active: #2ecc71;
    --status-at-risk: #f1c40f;
    --status-inactive: #e67e22;
    --status-churned: #e74c3c;
    --rune-blue: #5dade2;
}

/* Main app background */
.stApp {
    background: linear-gradient(180deg, #0d1520 0%, #1a2a3a 50%, #0d1520 100%);
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--parchment) 0%, var(--parchment-dark) 100%);
    border-right: 4px solid var(--driftwood);
}

[data-testid="stSidebar"] * {
    color: var(--driftwood-dark) !important;
}

[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    font-family: 'Cinzel', serif !important;
    color: var(--driftwood-dark) !important;
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

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    background: linear-gradient(180deg, var(--driftwood) 0%, var(--driftwood-dark) 100%);
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
    transition: all 0.2s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    background: rgba(255,215,0,0.2);
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(180deg, var(--gold-dark) 0%, #b8860b 100%) !important;
    color: var(--driftwood-dark) !important;
}

.stTabs [data-baseweb="tab-panel"] {
    background: linear-gradient(180deg, rgba(244,228,188,0.08) 0%, rgba(244,228,188,0.03) 100%);
    border: 2px solid var(--driftwood);
    border-top: none;
    border-radius: 0 0 8px 8px;
    padding: 20px;
}

/* Metrics */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, var(--driftwood) 0%, var(--driftwood-dark) 100%);
    border: 2px solid var(--gold-dark);
    border-radius: 10px;
    padding: 15px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.1);
}

[data-testid="stMetric"] label {
    font-family: 'Cinzel', serif !important;
    color: var(--gold) !important;
    font-size: 0.85rem !important;
}

[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-family: 'Crimson Text', serif !important;
    color: var(--parchment) !important;
    font-size: 1.5rem !important;
}

[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    font-family: 'Crimson Text', serif !important;
}

/* DataFrames */
[data-testid="stDataFrame"] {
    border: 3px solid var(--driftwood);
    border-radius: 8px;
    overflow: hidden;
}

/* Buttons */
.stButton > button {
    font-family: 'Cinzel', serif !important;
    background: linear-gradient(180deg, var(--gold) 0%, var(--gold-dark) 100%);
    color: var(--driftwood-dark) !important;
    border: 2px solid #b8860b;
    border-radius: 6px;
    font-weight: 600;
    box-shadow: 0 3px 6px rgba(0,0,0,0.3);
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(180deg, var(--gold-light) 0%, var(--gold) 100%);
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.4);
}

/* Forms */
[data-testid="stForm"] {
    background: linear-gradient(180deg, rgba(139,115,85,0.2) 0%, rgba(92,77,58,0.2) 100%);
    border: 2px solid var(--driftwood);
    border-radius: 8px;
    padding: 15px;
}

/* Select boxes */
.stSelectbox > div > div {
    background: var(--parchment-light) !important;
    border: 2px solid var(--driftwood) !important;
}

.stSelectbox > div > div > div {
    color: var(--driftwood-dark) !important;
}

.stSelectbox label {
    color: var(--parchment) !important;
}

[data-testid="stSidebar"] .stSelectbox label {
    color: var(--driftwood-dark) !important;
}

/* Inputs in sidebar */
[data-testid="stSidebar"] input {
    background: var(--parchment-light) !important;
    border: 2px solid var(--driftwood) !important;
    color: var(--driftwood-dark) !important;
}

/* Expanders */
.streamlit-expanderHeader {
    font-family: 'Cinzel', serif !important;
    background: linear-gradient(180deg, var(--driftwood) 0%, var(--driftwood-dark) 100%);
    border: 2px solid var(--gold-dark);
    border-radius: 6px;
    color: var(--gold) !important;
}

/* Link buttons */
.stLinkButton > a {
    font-family: 'Cinzel', serif !important;
    background: linear-gradient(180deg, var(--ocean) 0%, var(--ocean-dark) 100%);
    color: var(--parchment) !important;
    border: 2px solid var(--ocean-light);
}

/* Captions */
.stCaption {
    font-family: 'Crimson Text', serif !important;
    color: var(--parchment-dark) !important;
    font-style: italic;
}

/* Alerts */
.stAlert {
    font-family: 'Crimson Text', serif;
    border-radius: 6px;
}

/* Toast */
[data-testid="stToast"] {
    background: linear-gradient(180deg, var(--parchment) 0%, var(--parchment-dark) 100%);
    border: 2px solid var(--gold-dark);
    color: var(--driftwood-dark);
    font-family: 'Crimson Text', serif;
}

/* Horizontal rule */
hr {
    border-color: var(--driftwood) !important;
}

/* Spinner */
.stSpinner > div {
    border-color: var(--gold) !important;
}

/* Progress bars */
.stProgress > div > div {
    background-color: var(--gold-dark) !important;
}

/* Status badges */
.status-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 12px;
    font-family: 'Cinzel', serif;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.status-active { background: var(--status-active); color: white; }
.status-at-risk { background: var(--status-at-risk); color: #333; }
.status-inactive { background: var(--status-inactive); color: white; }
.status-churned { background: var(--status-churned); color: white; }

/* Member cards */
.member-card {
    background: linear-gradient(145deg, var(--driftwood) 0%, var(--driftwood-dark) 100%);
    border: 2px solid var(--gold-dark);
    border-radius: 10px;
    padding: 12px;
    margin: 4px 0;
    display: flex;
    align-items: center;
    gap: 12px;
}

.member-card .username {
    color: var(--parchment);
    font-family: 'Cinzel', serif;
    font-size: 0.95rem;
    font-weight: 600;
}

.member-card .stats {
    color: var(--parchment-dark);
    font-family: 'Crimson Text', serif;
    font-size: 0.85rem;
}

/* Health score gauge */
.health-gauge {
    background: linear-gradient(145deg, var(--driftwood) 0%, var(--driftwood-dark) 100%);
    border: 3px solid var(--gold-dark);
    border-radius: 50%;
    width: 120px;
    height: 120px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: 0 auto;
}

.health-gauge .score {
    font-family: 'Cinzel', serif;
    font-size: 2rem;
    color: var(--gold);
    font-weight: 700;
}

.health-gauge .label {
    font-family: 'Crimson Text', serif;
    font-size: 0.8rem;
    color: var(--parchment-dark);
}

/* Info cards */
.info-card {
    background: linear-gradient(145deg, var(--driftwood) 0%, var(--driftwood-dark) 100%);
    border: 2px solid var(--gold-dark);
    border-radius: 10px;
    padding: 15px;
    text-align: center;
}

.info-card .title {
    color: var(--gold);
    font-family: 'Cinzel', serif;
    font-size: 0.85rem;
    margin-bottom: 8px;
}

.info-card .value {
    color: var(--parchment);
    font-family: 'Crimson Text', serif;
    font-size: 1.2rem;
    font-weight: 600;
}

/* Mobile responsiveness */
@media screen and (max-width: 768px) {
    .stApp {
        padding: 0.5rem;
    }
    
    [data-testid="stSidebar"] {
        min-width: 250px;
    }
    
    [data-testid="stDataFrame"] {
        font-size: 0.85rem;
    }
    
    [data-testid="stMetric"] {
        padding: 10px;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        overflow-x: auto;
        flex-wrap: nowrap;
        -webkit-overflow-scrolling: touch;
    }
    
    .stTabs [data-baseweb="tab"] {
        flex-shrink: 0;
        padding: 8px 12px;
    }
    
    .stApp h1 { font-size: 1.5rem !important; }
    .stApp h2 { font-size: 1.25rem !important; }
    .stApp h3 { font-size: 1.1rem !important; }
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--driftwood-dark);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: var(--gold-dark);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--gold);
}
</style>
"""
