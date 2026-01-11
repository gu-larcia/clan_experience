# Clan Analytics Dashboard v2.0

A modern, clean analytics dashboard for tracking OSRS clan activity, XP progression, and member churn using the [WiseOldMan](https://wiseoldman.net/) API.

## What's New in v2.0

- **Full Member Roster Support**: Now loads ALL clan members (not just 20) via API key authentication
- **Modern UI Design**: Clean, professional interface suitable for non-OSRS audiences
- **API Key Integration**: Built-in support for WOM API key (100 req/min vs 20 req/min)
- **Improved Charts**: Fresh color palette and better data visualization
- **API Status Indicator**: Shows rate limit status and member count

## Features

- **Activity Tracking**: Classify members as Active, At Risk, Inactive, or Churned based on last XP gain
- **Clan Health Score**: Aggregate metric showing overall clan engagement
- **XP Gains Analysis**: Track skill/boss gains over configurable time periods
- **Churn Risk Detection**: Identify members who may be leaving the game
- **Achievement Feed**: Recent milestones achieved by clan members
- **Competition Tracking**: View active and past clan competitions

## Tech Stack

- **Python 3.11+**
- **Streamlit** - Interactive web dashboard
- **Plotly** - Data visualization
- **Pandas** - Data manipulation
- **WiseOldMan API v2** - OSRS player/group data

## Project Structure

```
wom_tracker_v2/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── config/                # Application settings
│   ├── __init__.py
│   └── settings.py        # API URLs, cache TTLs, thresholds, API key
├── services/              # Business logic
│   ├── __init__.py
│   ├── api.py             # WiseOldMan API client
│   └── activity.py        # Activity analysis & churn detection
├── ui/                    # User interface
│   ├── __init__.py
│   ├── styles.py          # Modern CSS styling
│   ├── charts.py          # Plotly chart functions
│   └── components.py      # HTML components
└── utils/                 # Utilities
    ├── __init__.py
    └── formatting.py      # XP/time formatting helpers
```

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd wom_tracker_v2

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Configuration

### API Key Setup (Important!)

The API key is **never stored in code** - it's loaded from Streamlit's secrets management.

**For Local Development:**
1. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`
2. Add your actual API key:
   ```toml
   WOM_API_KEY = "your-actual-api-key"
   ```
3. The `.gitignore` ensures this file is never committed

**For Streamlit Cloud Deployment:**
1. Go to your app's dashboard on Streamlit Cloud
2. Click "Settings" → "Secrets"
3. Add your secret:
   ```toml
   WOM_API_KEY = "your-actual-api-key"
   ```

Without an API key, the app still works but with limited rate limits (20 req/min instead of 100 req/min).

### Changing the Tracked Clan

Edit `config/settings.py`:
```python
WOM_GROUP_ID = 11625  # Change to your group ID
```

Find your group ID on [wiseoldman.net/groups](https://wiseoldman.net/groups).

### Activity Thresholds

Default classification thresholds (days since last XP gain):
- **Active**: 0-7 days
- **At Risk**: 8-30 days
- **Inactive**: 31-90 days
- **Churned**: 90+ days

These can be adjusted in settings or via the sidebar.

## API Rate Limits

WiseOldMan API limits:
- **Without API key**: 20 requests per minute
- **With API key**: 100 requests per minute

**Important**: Per WOM guidelines, use 1-6 hour intervals for player updates to avoid IP bans.

## Deployment

### Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Connect repository to [Streamlit Cloud](https://streamlit.io/cloud)
3. Add `WOM_API_KEY` to secrets
4. Deploy

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

## Credits

- [WiseOldMan](https://wiseoldman.net/) - Player tracking API
- Built with Streamlit and Plotly

## License

MIT
