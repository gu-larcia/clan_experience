# WOM Clan Analytics Dashboard

Streamlit dashboard for tracking OSRS clan activity via the [WiseOldMan](https://wiseoldman.net/) API.

## Features

- Activity classification (Active / At Risk / Inactive / Churned)
- Clan health score
- XP gains tracking by skill and time period
- Churn risk detection
- Achievement feed

## Quick Start

```bash
# Clone and setup
git clone <your-repo>
cd wom_dashboard

# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## Configuration

Edit `config.py` to change:

```python
DEFAULT_GROUP_ID = 139  # Your WOM group ID
```

Find your group ID at https://wiseoldman.net/groups

### API Key (Optional)

For higher rate limits (100 req/min vs 20 req/min), get an API key from the [WOM Discord](https://wiseoldman.net/discord).

**Local development** — create `.streamlit/secrets.toml`:

```toml
WOM_API_KEY = "your-key-here"
```

**Streamlit Cloud** — add to app secrets in the dashboard.

## Project Structure

```
wom_dashboard/
├── app.py          # Main Streamlit app
├── api.py          # WOM API client
├── analysis.py     # Activity classification
├── charts.py       # Plotly visualizations
├── styles.py       # CSS theming
├── config.py       # Settings
└── requirements.txt
```

## API Notes

The WOM API v2 does not have a `/groups/{id}/members` endpoint. Member data is retrieved via `/groups/{id}/hiscores?metric=overall`, which returns all members with no pagination limit.

Key endpoints:
- `GET /groups/{id}` — group details
- `GET /groups/{id}/hiscores` — all members with stats
- `GET /groups/{id}/gained` — XP gains
- `GET /groups/{id}/achievements` — recent achievements

Docs: https://docs.wiseoldman.net/api

## Deployment

### Streamlit Cloud

1. Push to GitHub
2. Connect repo at [share.streamlit.io](https://share.streamlit.io)
3. Set `WOM_API_KEY` secret (optional)
4. Deploy

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

## License

MIT
