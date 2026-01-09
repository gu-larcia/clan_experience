"""WiseOldMan API v2 client.

API docs: https://docs.wiseoldman.net/api

Key endpoints used:
    GET /groups/:id              - Group details
    GET /groups/:id/hiscores     - All members with stats (no pagination)
    GET /groups/:id/gained       - XP gains for all members
    GET /groups/:id/achievements - Recent achievements
    GET /groups/:id/competitions - Group competitions

Note: There is NO /groups/:id/members endpoint. Use /hiscores instead.
"""

import requests
from datetime import datetime
from typing import Any


class WOMClient:
    """Synchronous client for WiseOldMan API v2."""

    def __init__(self, base_url: str, api_key: str | None = None, user_agent: str = "WOM-Client/1.0"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers["User-Agent"] = user_agent
        if api_key:
            self.session.headers["x-api-key"] = api_key

    def _get(self, endpoint: str, params: dict | None = None) -> Any:
        """Execute GET request. Raises on HTTP errors."""
        url = f"{self.base_url}{endpoint}"
        resp = self.session.get(url, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_group(self, group_id: int) -> dict:
        """Fetch group details."""
        return self._get(f"/groups/{group_id}")

    def get_members(self, group_id: int) -> list[dict]:
        """
        Fetch all group members via hiscores endpoint.
        
        Returns list of dicts with 'player' and 'data' keys.
        The 'player' object contains: id, username, displayName, exp, ehp, ehb,
        lastChangedAt, updatedAt, type, build, etc.
        """
        return self._get(f"/groups/{group_id}/hiscores", params={"metric": "overall"})

    def get_gains(self, group_id: int, metric: str = "overall", period: str = "week") -> list[dict]:
        """
        Fetch XP/KC gains for all members.
        
        Args:
            metric: Skill name, boss name, 'overall', 'ehp', or 'ehb'
            period: 'day', 'week', 'month', or 'year'
        """
        return self._get(f"/groups/{group_id}/gained", params={"metric": metric, "period": period})

    def get_achievements(self, group_id: int, limit: int = 50) -> list[dict]:
        """Fetch recent group achievements."""
        return self._get(f"/groups/{group_id}/achievements", params={"limit": limit})

    def get_competitions(self, group_id: int) -> list[dict]:
        """Fetch group competitions (past and current)."""
        return self._get(f"/groups/{group_id}/competitions")


def parse_datetime(value: str | None) -> datetime | None:
    """Parse ISO datetime string from WOM API."""
    if not value:
        return None
    try:
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        return datetime.fromisoformat(value)
    except (ValueError, AttributeError):
        return None
