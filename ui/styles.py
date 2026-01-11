"""Modern, clean CSS for Clan Analytics Dashboard."""

MODERN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg-primary: #0f172a;
    --bg-secondary: #1e293b;
    --bg-tertiary: #334155;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --accent-primary: #3b82f6;
    --accent-secondary: #8b5cf6;
    --border-color: #334155;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --info: #06b6d4;
}

/* Main app background */
.stApp {
    background: linear-gradient(135deg, var(--bg-primary) 0%, #1a1f35 100%);
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: var(--bg-secondary);
    border-right: 1px solid var(--border-color);
}

[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    font-family: 'Inter', sans-serif !important;
    color: var(--text-primary) !important;
    font-weight: 600;
}

/* Headers */
.stApp h1, .stApp h2, .stApp h3 {
    font-family: 'Inter', sans-serif !important;
    color: var(--text-primary) !important;
    font-weight: 600;
}

.stApp h1 {
    font-size: 1.875rem;
    letter-spacing: -0.025em;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-secondary);
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid var(--border-color);
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif !important;
    color: var(--text-secondary) !important;
    background: transparent;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 500;
    font-size: 0.875rem;
    transition: all 0.2s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    background: var(--bg-tertiary);
    color: var(--text-primary) !important;
}

.stTabs [aria-selected="true"] {
    background: var(--accent-primary) !important;
    color: white !important;
}

.stTabs [data-baseweb="tab-panel"] {
    background: transparent;
    padding: 24px 0;
}

/* Metrics */
[data-testid="stMetric"] {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 20px;
}

[data-testid="stMetric"] label {
    font-family: 'Inter', sans-serif !important;
    color: var(--text-secondary) !important;
    font-size: 0.75rem !important;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-family: 'Inter', sans-serif !important;
    color: var(--text-primary) !important;
    font-size: 1.5rem !important;
    font-weight: 700;
}

[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    font-family: 'Inter', sans-serif !important;
}

/* DataFrames */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border-color);
    border-radius: 12px;
    overflow: hidden;
}

/* Buttons */
.stButton > button {
    font-family: 'Inter', sans-serif !important;
    background: var(--accent-primary);
    color: white !important;
    border: none;
    border-radius: 8px;
    font-weight: 500;
    padding: 0.5rem 1rem;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: #2563eb;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

/* Select boxes */
.stSelectbox > div > div {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
}

.stSelectbox > div > div > div {
    color: var(--text-primary) !important;
}

.stSelectbox label {
    color: var(--text-secondary) !important;
    font-size: 0.875rem;
    font-weight: 500;
}

/* Multi-select */
.stMultiSelect > div > div {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
}

.stMultiSelect label {
    color: var(--text-secondary) !important;
}

/* Expanders */
.streamlit-expanderHeader {
    font-family: 'Inter', sans-serif !important;
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    color: var(--text-primary) !important;
    font-weight: 500;
}

/* Link buttons */
.stLinkButton > a {
    font-family: 'Inter', sans-serif !important;
    background: var(--bg-secondary);
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color);
    border-radius: 8px;
}

.stLinkButton > a:hover {
    background: var(--bg-tertiary);
    border-color: var(--accent-primary);
}

/* Captions */
.stCaption {
    font-family: 'Inter', sans-serif !important;
    color: var(--text-muted) !important;
}

/* Alerts */
.stAlert {
    font-family: 'Inter', sans-serif;
    border-radius: 8px;
}

/* Dividers */
hr {
    border-color: var(--border-color) !important;
    margin: 1.5rem 0;
}

/* Spinner */
.stSpinner > div {
    border-color: var(--accent-primary) !important;
}

/* Progress bars */
.stProgress > div > div {
    background-color: var(--accent-primary) !important;
}

/* Number inputs */
.stNumberInput > div > div > input {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border-color) !important;
    color: var(--text-primary) !important;
    border-radius: 8px;
}

.stNumberInput label {
    color: var(--text-secondary) !important;
}

/* Sliders */
.stSlider > div > div > div {
    background: var(--accent-primary) !important;
}

.stSlider label {
    color: var(--text-secondary) !important;
}

/* Cards - Custom component styling */
.metric-card {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 20px;
}

.metric-card .label {
    color: var(--text-secondary);
    font-size: 0.75rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
}

.metric-card .value {
    color: var(--text-primary);
    font-size: 1.5rem;
    font-weight: 700;
}

.metric-card .subtitle {
    color: var(--text-muted);
    font-size: 0.75rem;
    margin-top: 4px;
}

/* Status badges */
.status-badge {
    display: inline-flex;
    align-items: center;
    padding: 4px 12px;
    border-radius: 9999px;
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem;
    font-weight: 500;
}

.status-active { background: rgba(16, 185, 129, 0.15); color: #10b981; }
.status-at-risk { background: rgba(245, 158, 11, 0.15); color: #f59e0b; }
.status-inactive { background: rgba(249, 115, 22, 0.15); color: #f97316; }
.status-churned { background: rgba(239, 68, 68, 0.15); color: #ef4444; }

/* Health score gauge */
.health-gauge {
    background: var(--bg-secondary);
    border: 3px solid;
    border-radius: 50%;
    width: 140px;
    height: 140px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: 0 auto;
}

.health-gauge .score {
    font-family: 'Inter', sans-serif;
    font-size: 2.5rem;
    font-weight: 700;
    line-height: 1;
}

.health-gauge .label {
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem;
    color: var(--text-secondary);
    margin-top: 4px;
    font-weight: 500;
}

/* At-risk cards */
.risk-card {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-left: 4px solid;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 8px 0;
}

/* Toast */
[data-testid="stToast"] {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    font-family: 'Inter', sans-serif;
    border-radius: 8px;
}

/* Mobile responsiveness */
@media screen and (max-width: 768px) {
    .stApp {
        padding: 0.5rem;
    }
    
    [data-testid="stSidebar"] {
        min-width: 280px;
    }
    
    [data-testid="stDataFrame"] {
        font-size: 0.85rem;
    }
    
    [data-testid="stMetric"] {
        padding: 12px;
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
    background: var(--bg-secondary);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: var(--bg-tertiary);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--text-muted);
}
</style>
"""
