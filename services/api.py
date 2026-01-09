"""WiseOldMan API client."""

import requests
from typing import Dict, List, Optional, Any
from datetime import datetime


class WOMClient:
    """Client for WiseOldMan API v2."""
    
    def __init__(
        self, 
        base_url: str = "https://api.wiseoldman.net/v2",
        api_key: Optional[str] = None,
        user_agent: str = "OSRS-Clan-Tracker/1.0"
    ):
        self.base_url = base_url
        self._session = requests.Session()
        
        headers = {'User-Agent': user_agent}
        if api_key:
            headers['x-api-key'] = api_key
        
        self._session.headers.update(headers)
    
    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        """Make GET request to API."""
        url = f"{self.base_url}{endpoint}"
        response = self._session.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    
    # ===== Group Endpoints =====
    
    def get_group_details(self, group_id: int) -> Dict:
        """
        Get group details including member count, description, etc.
        
        Returns: {
            id, name, clanChat, description, homeworld, verified,
            memberCount, createdAt, updatedAt, patron, profileImage, bannerImage
        }
        """
        return self._get(f"/groups/{group_id}")
    
    def get_group_members(self, group_id: int) -> List[Dict]:
        """
        Get all group members with their current stats.
        
        Uses the hiscores endpoint which returns all members with player data.
        
        Returns list of: {
            player: {id, username, displayName, type, build, country, status,
                     patron, exp, ehp, ehb, ttm, tt200m, registeredAt, updatedAt,
                     lastChangedAt, lastImportedAt},
            data: {rank, level, experience}
        }
        """
        # The hiscores endpoint returns all members with their stats
        # It accepts a metric parameter (default: overall)
        hiscores = self._get(f"/groups/{group_id}/hiscores", params={"metric": "overall"})
        
        # Transform to match expected member format
        # The hiscores response has player data, we need to add membership info
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
    
    def get_group_hiscores(
        self, 
        group_id: int, 
        metric: str = "overall"
    ) -> List[Dict]:
        """
        Get group hiscores for a specific metric.
        
        Args:
            group_id: Group ID
            metric: Skill name or 'overall', 'ehp', 'ehb'
            
        Returns list of: {
            player: {...}, data: {rank, level/kills/score, experience/value}
        }
        """
        return self._get(f"/groups/{group_id}/hiscores", params={"metric": metric})
    
    def get_group_gains(
        self,
        group_id: int,
        metric: str = "overall",
        period: str = "week"
    ) -> List[Dict]:
        """
        Get XP/KC gains for group members over a time period.
        
        Args:
            group_id: Group ID
            metric: Skill name, boss name, or 'overall', 'ehp', 'ehb'
            period: 'day', 'week', 'month', 'year'
            
        Returns list of: {
            player: {...}, data: {gained, start, end}
        }
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
        """
        Get recent group achievements.
        
        Returns list of: {
            playerId, name, metric, threshold, accuracy, createdAt, player: {...}
        }
        """
        return self._get(
            f"/groups/{group_id}/achievements",
            params={"limit": limit}
        )
    
    def get_group_competitions(self, group_id: int) -> List[Dict]:
        """
        Get group competitions (past and current).
        
        Returns list of competition objects with participants.
        """
        return self._get(f"/groups/{group_id}/competitions")
    
    def get_group_activity(
        self,
        group_id: int,
        limit: int = 50
    ) -> List[Dict]:
        """
        Get group activity feed (joins, leaves, role changes).
        
        Returns list of: {
            groupId, playerId, type, role, previousRole, createdAt, player: {...}
        }
        """
        return self._get(
            f"/groups/{group_id}/activity",
            params={"limit": limit}
        )
    
    # ===== Player Endpoints =====
    
    def get_player(self, username: str) -> Dict:
        """Get player details by username."""
        return self._get(f"/players/{username}")
    
    def get_player_gains(
        self,
        username: str,
        period: str = "week"
    ) -> Dict:
        """
        Get player XP gains over a period.
        
        Returns: {startsAt, endsAt, data: {skills: {...}, bosses: {...}, ...}}
        """
        return self._get(
            f"/players/{username}/gained",
            params={"period": period}
        )
    
    def get_player_snapshots(
        self,
        username: str,
        period: str = "week"
    ) -> List[Dict]:
        """
        Get player snapshot history.
        
        Returns list of snapshot objects with full stats at each point.
        """
        return self._get(
            f"/players/{username}/snapshots",
            params={"period": period}
        )
    
    def update_player(self, username: str) -> Dict:
        """
        Request a player update (fetches latest from hiscores).
        
        Note: This counts against rate limits more heavily.
        """
        url = f"{self.base_url}/players/{username}"
        response = self._session.post(url, timeout=30)
        response.raise_for_status()
        return response.json()
    
    # ===== Utility Methods =====
    
    def search_groups(self, name: str, limit: int = 20) -> List[Dict]:
        """Search for groups by name."""
        return self._get("/groups", params={"name": name, "limit": limit})
    
    def get_global_leaderboard(
        self,
        metric: str = "overall",
        player_type: str = "regular"
    ) -> List[Dict]:
        """Get global hiscores."""
        return self._get(
            "/players",
            params={"metric": metric, "playerType": player_type}
        )


def parse_wom_datetime(dt_string: Optional[str]) -> Optional[datetime]:
    """Parse WOM API datetime string to datetime object."""
    if not dt_string:
        return None
    
    # WOM uses ISO format with Z suffix
    try:
        # Handle both formats
        if dt_string.endswith('Z'):
            dt_string = dt_string[:-1] + '+00:00'
        return datetime.fromisoformat(dt_string)
    except (ValueError, AttributeError):
        return None
