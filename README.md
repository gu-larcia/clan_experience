# WiseOldMan Clan Analytics Dashboard

A Streamlit dashboard for tracking OSRS clan activity, XP progression, and member churn using the [WiseOldMan](https://wiseoldman.net/) API.

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
wom_tracker/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── config/                # Application settings
│   ├── __init__.py
│   └── settings.py        # API URLs, cache TTLs, thresholds
├── services/              # Business logic
│   ├── __init__.py
│   ├── api.py             # WiseOldMan API client
│   └── activity.py        # Activity analysis & churn detection
├── ui/                    # User interface
│   ├── __init__.py
│   ├── styles.py          # OSRS-themed CSS
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
cd wom_tracker

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

### Environment Variables / Secrets

For higher API rate limits (100 req/min vs 20 req/min), add a WiseOldMan API key:

**Local development** - Create `.streamlit/secrets.toml`:
```toml
WOM_API_KEY = "your-api-key-here"
```

**Streamlit Cloud** - Add to app secrets in the dashboard.

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

Request an API key via the [WOM Discord](https://discord.gg/wiseoldman).

## Deployment

### Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Connect repository to [Streamlit Cloud](https://streamlit.io/cloud)
3. Add `WOM_API_KEY` to secrets (optional)
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

## Future Enhancements

- [ ] PostgreSQL integration for historical data storage
- [ ] Member comparison tools
- [ ] Scheduled data refresh (GitHub Actions)
- [ ] Discord webhook notifications for churn alerts
- [ ] Individual player deep-dive pages
- [ ] Export to CSV/Excel

## Credits

- [WiseOldMan](https://wiseoldman.net/) - Player tracking API
- [OSRS Wiki](https://oldschool.runescape.wiki/) - Icons and game data
- Design inspired by the OSRS aesthetic

## License

MIT
