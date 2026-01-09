"""WiseOldMan API v2 client.

API docs: https://docs.wiseoldman.net/api

Key endpoints:
    GET /groups/:id              - Group details (includes memberCount)
    GET /groups/:id/memberships  - All members with membership status
    GET /groups/:id/hiscores     - Members with tracked stats (no limit)
    GET /groups/:id/gained       - XP gains for all members
    GET /groups/:id/achievements - Recent achievements
    GET /groups/:id/activity     - Join/leave/role change history
    GET /groups/:id/competitions - Group competitions
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

    def _try_get(self, endpoint: str, params: dict | None = None) -> Any | None:
        """Execute GET request, return None on 404."""
        try:
            return self._get(endpoint, params)
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise

    def get_group(self, group_id: int) -> dict:
        """Fetch group details including memberCount."""
        return self._get(f"/groups/{group_id}")

    def get_memberships(self, group_id: int) -> list[dict] | None:
        """
        Fetch all group memberships (if endpoint exists).
        
        Returns all members with their membership status, or None if 
        endpoint doesn't exist.
        """
        return self._try_get(f"/groups/{group_id}/memberships")

    def get_hiscores(self, group_id: int, metric: str = "overall") -> list[dict]:
        """
        Fetch group hiscores. Returns members who have tracked stats.
        
        Note: Only includes members whose stats have been tracked.
        May not include all group members.
        """
        return self._get(f"/groups/{group_id}/hiscores", params={"metric": metric})

    def get_members(self, group_id: int) -> list[dict]:
        """
        Fetch all group members.
        
        Tries /memberships first (returns all members with status),
        falls back to /hiscores (only tracked members).
        
        Returns list of dicts with 'player' and optional 'membership' keys.
        """
        # Try memberships endpoint first (includes all members)
        memberships = self.get_memberships(group_id)
        if memberships is not None:
            return memberships
        
        # Fall back to hiscores (only tracked members)
        return self.get_hiscores(group_id, metric="overall")

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

    def get_activity(self, group_id: int, limit: int = 100) -> list[dict]:
        """
        Fetch group activity feed.
        
        Returns join/leave/role change events. Useful for tracking
        former members (kicked, banned, left).
        """
        return self._get(f"/groups/{group_id}/activity", params={"limit": limit})


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
