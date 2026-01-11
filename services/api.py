"""WiseOldMan API client with pagination support."""

import requests
from typing import Dict, List, Optional, Any
from datetime import datetime


class WOMClient:
    """Client for WiseOldMan API v2."""

    def __init__(
        self,
        base_url: str = "https://api.wiseoldman.net/v2",
        api_key: Optional[str] = None,
        user_agent: str = "Clan-Analytics-Dashboard/2.0"
    ):
        self.base_url = base_url
        self._session = requests.Session()
        self.api_key = api_key

        headers = {'User-Agent': user_agent}
        if api_key:
            headers['x-api-key'] = api_key

        self._session.headers.update(headers)

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        """Execute GET request."""
        url = f"{self.base_url}{endpoint}"
        response = self._session.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_group_details(self, group_id: int) -> Dict:
        """
        Fetch group metadata.

        Returns dict with: id, name, clanChat, description, homeworld,
        verified, memberCount, createdAt, updatedAt, patron, profileImage,
        bannerImage
        """
        return self._get(f"/groups/{group_id}")

    def get_group_members(self, group_id: int) -> List[Dict]:
        """
        Fetch all group members with current stats.

        Uses the hiscores endpoint which returns all members ranked by XP.
        The WOM API returns complete member lists without pagination limits
        when using the hiscores endpoint.

        Returns list of dicts with player data and membership info.
        """
        hiscores = self._get(
            f"/groups/{group_id}/hiscores",
            params={"metric": "overall"}
        )

        members = []
        for entry in hiscores:
            player = entry.get("player", {})
            members.append({
                "player": player,
                "membership": {
                    "playerId": player.get("id"),
                    "groupId": group_id,
                    "role": entry.get("role", "member"),
                    "createdAt": player.get("registeredAt"),
                    "updatedAt": player.get("updatedAt"),
                }
            })
        return members

    def get_group_members_paginated(self, group_id: int) -> List[Dict]:
        """
        Fetch all members using pagination on the members endpoint.

        Use this as a fallback if hiscores endpoint does not return all
        members. Fetches in batches of 50 until no more results.
        """
        all_members = []
        offset = 0
        limit = 50

        while True:
            response = self._get(
                f"/groups/{group_id}/members",
                params={"limit": limit, "offset": offset}
            )

            members = response if isinstance(response, list) else response.get("members", [])

            if not members:
                break

            all_members.extend(members)
            offset += limit

            # Safety check to avoid infinite loops
            if len(members) < limit:
                break

        return all_members

    def get_group_hiscores(
        self,
        group_id: int,
        metric: str = "overall"
    ) -> List[Dict]:
        """
        Fetch group hiscores for a metric.

        Returns all members ranked by the specified metric.
        """
        return self._get(
            f"/groups/{group_id}/hiscores",
            params={"metric": metric}
        )

    def get_group_gains(
        self,
        group_id: int,
        metric: str = "overall",
        period: str = "week"
    ) -> List[Dict]:
        """
        Fetch XP/KC gains over a time period.

        Args:
            group_id: Group ID
            metric: Skill name, boss name, or 'overall', 'ehp', 'ehb'
            period: 'day', 'week', 'month', 'year'

        Returns list with player data and gains info.
        """
        return self._get(
            f"/groups/{group_id}/gained",
            params={"metric": metric, "period": period}
        )

    def get_group_achievements(
        self,
        group_id: int,
        limit: int = 50
    ) -> List[Dict]:
        """Fetch recent group achievements."""
        return self._get(
            f"/groups/{group_id}/achievements",
            params={"limit": limit}
        )

    def get_group_competitions(self, group_id: int) -> List[Dict]:
        """Fetch group competitions."""
        return self._get(f"/groups/{group_id}/competitions")

    def get_group_activity(
        self,
        group_id: int,
        limit: int = 50
    ) -> List[Dict]:
        """Fetch group activity feed (joins, leaves, role changes)."""
        return self._get(
            f"/groups/{group_id}/activity",
            params={"limit": limit}
        )

    def get_player(self, username: str) -> Dict:
        """Fetch player details by username."""
        return self._get(f"/players/{username}")

    def get_player_gains(
        self,
        username: str,
        period: str = "week"
    ) -> Dict:
        """Fetch player XP gains over a period."""
        return self._get(
            f"/players/{username}/gained",
            params={"period": period}
        )

    def get_player_snapshots(
        self,
        username: str,
        period: str = "week"
    ) -> List[Dict]:
        """Fetch player snapshot history."""
        return self._get(
            f"/players/{username}/snapshots",
            params={"period": period}
        )

    def update_player(self, username: str) -> Dict:
        """
        Request player update from hiscores.

        Use sparingly (1-6 hour intervals) to avoid IP bans.
        """
        url = f"{self.base_url}/players/{username}"
        response = self._session.post(url, timeout=30)
        response.raise_for_status()
        return response.json()

    def search_groups(self, name: str, limit: int = 20) -> List[Dict]:
        """Search groups by name."""
        return self._get("/groups", params={"name": name, "limit": limit})

    def get_rate_limit_status(self) -> Dict[str, str]:
        """Return API key status info."""
        return {
            "has_api_key": bool(self.api_key),
            "rate_limit": "100 req/min" if self.api_key else "20 req/min",
        }


def parse_wom_datetime(dt_string: Optional[str]) -> Optional[datetime]:
    """Parse WOM API datetime string to datetime object."""
    if not dt_string:
        return None

    try:
        if dt_string.endswith('Z'):
            dt_string = dt_string[:-1] + '+00:00'
        return datetime.fromisoformat(dt_string)
    except (ValueError, AttributeError):
        return None
