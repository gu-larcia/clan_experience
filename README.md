# Clan Analytics Dashboard v2.0

Analytics dashboard for OSRS clan tracking using the WiseOldMan API.

## Features

- Activity tracking with member classification (Active, At Risk, Inactive, Churned)
- Clan health score aggregation
- XP gains analysis across configurable time periods
- Churn risk detection and member filtering
- Achievement feed display
- Competition tracking

## Stack

- Python 3.11+
- Streamlit
- Plotly
- Pandas
- WiseOldMan API v2

## Project Structure

```
wom_tracker/
├── app.py                 # Main application
├── requirements.txt
├── config/
│   ├── __init__.py
│   └── settings.py        # API config, thresholds, constants
├── services/
│   ├── __init__.py
│   ├── api.py             # WOM API client
│   └── activity.py        # Activity analysis
├── ui/
│   ├── __init__.py
│   ├── styles.py          # CSS
│   ├── charts.py          # Plotly charts
│   └── components.py      # HTML components
└── utils/
    ├── __init__.py
    └── formatting.py      # Display formatters
```

## Installation

```bash
git clone <repository-url>
cd wom_tracker

python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

pip install -r requirements.txt
streamlit run app.py
```

## Configuration

### API Key

API keys are loaded from Streamlit secrets. Never commit keys to code.

**Local development:**
1. Create `.streamlit/secrets.toml`
2. Add: `WOM_API_KEY = "your-key"`
3. File is gitignored

**Streamlit Cloud:**
1. Settings > Secrets
2. Add: `WOM_API_KEY = "your-key"`

Without a key, rate limits are 20 req/min. With a key: 100 req/min.

### Group ID

Edit `config/settings.py`:
```python
WOM_GROUP_ID = 11625  # Your group ID
```

Find your ID at wiseoldman.net/groups.

### Activity Thresholds

Default classification (days since last XP gain):
- Active: 0-7 days
- At Risk: 8-30 days
- Inactive: 31-90 days
- Churned: 90+ days

Adjustable in settings or via sidebar.

## API Rate Limits

WiseOldMan enforces:
- Without key: 20 requests/minute
- With key: 100 requests/minute

Use 1-6 hour intervals for automated updates to avoid IP bans.

## Deployment

### Streamlit Cloud

1. Push to GitHub
2. Connect at streamlit.io/cloud
3. Add WOM_API_KEY to secrets
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

## License

MIT
