"""Activity analysis and classification."""

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class MemberStatus:
    """Activity classification for a single member."""
    status: str  # active, at_risk, inactive, churned, unknown
    days_inactive: int
    color: str


def classify_member(
    last_changed: datetime | None,
    thresholds: dict[str, int],
    colors: dict[str, str],
) -> MemberStatus:
    """
    Classify a member's activity status based on last XP change.
    
    Args:
        last_changed: Datetime of last recorded XP gain
        thresholds: Dict with 'active', 'at_risk', 'inactive' day limits
        colors: Dict mapping status to hex color
    """
    if not last_changed:
        return MemberStatus("unknown", -1, colors.get("unknown", "#95a5a6"))

    now = datetime.now(timezone.utc)
    if last_changed.tzinfo is None:
        last_changed = last_changed.replace(tzinfo=timezone.utc)

    days = (now - last_changed).days

    if days <= thresholds["active"]:
        status = "active"
    elif days <= thresholds["at_risk"]:
        status = "at_risk"
    elif days <= thresholds["inactive"]:
        status = "inactive"
    else:
        status = "churned"

    return MemberStatus(status, days, colors.get(status, "#95a5a6"))


def analyze_members(
    raw_members: list[dict],
    thresholds: dict[str, int],
    colors: dict[str, str],
) -> dict:
    """
    Analyze all members and return aggregated stats.
    
    Args:
        raw_members: List from WOM API (may include untracked members)
        thresholds: Activity threshold days
        colors: Status color mapping
        
    Returns:
        Dict with members list, counts, totals, and health score
    """
    from api import parse_datetime

    counts = {"active": 0, "at_risk": 0, "inactive": 0, "churned": 0, "unknown": 0, "untracked": 0}
    totals = {"xp": 0, "ehp": 0.0, "ehb": 0.0}
    members = []

    for entry in raw_members:
        player = entry.get("player", {})
        
        # Check for untracked members (no stats in WOM)
        player_status = player.get("status", "active")
        xp = player.get("exp")
        
        if player_status == "untracked" or xp is None:
            # Untracked member - no stats available
            members.append({
                "username": player.get("displayName") or player.get("username") or "Unknown",
                "player_id": player.get("id"),
                "role": entry.get("membership", {}).get("role") or entry.get("role", "member"),
                "xp": 0,
                "ehp": 0,
                "ehb": 0,
                "type": player.get("type", "unknown"),
                "build": player.get("build", "unknown"),
                "status": "untracked",
                "days_inactive": -1,
                "color": colors.get("untracked", "#6c757d"),
                "last_changed": None,
            })
            counts["untracked"] += 1
            continue
        
        # Parse activity timestamp
        last_changed = parse_datetime(player.get("lastChangedAt"))
        status = classify_member(last_changed, thresholds, colors)
        counts[status.status] += 1

        # Aggregate totals
        ehp = player.get("ehp") or 0.0
        ehb = player.get("ehb") or 0.0
        totals["xp"] += xp
        totals["ehp"] += ehp
        totals["ehb"] += ehb

        members.append({
            "username": player.get("displayName") or player.get("username") or "Unknown",
            "player_id": player.get("id"),
            "role": entry.get("role", "member"),
            "xp": xp,
            "ehp": ehp,
            "ehb": ehb,
            "type": player.get("type", "regular"),
            "build": player.get("build", "main"),
            "status": status.status,
            "days_inactive": status.days_inactive,
            "color": status.color,
            "last_changed": last_changed,
        })

    total = len(members) or 1
    tracked = total - counts["untracked"]
    
    # Health score based on tracked members only
    weights = {"active": 100, "at_risk": 50, "inactive": 20, "churned": 0, "unknown": 25}
    if tracked > 0:
        health = sum(counts[s] * weights[s] for s in weights) / tracked
    else:
        health = 0

    return {
        "members": members,
        "counts": counts,
        "percentages": {k: v / total * 100 for k, v in counts.items()},
        "totals": totals,
        "averages": {k: v / tracked if tracked > 0 else 0 for k, v in totals.items()},
        "health_score": health,
        "total_members": total,
        "tracked_members": tracked,
    }


def get_at_risk_members(members: list[dict], min_days: int = 14, max_days: int = 90) -> list[dict]:
    """Filter members who are at risk of churning."""
    return sorted(
        [m for m in members if min_days <= m["days_inactive"] <= max_days],
        key=lambda x: x["days_inactive"],
        reverse=True,
    )


def get_retention_rates(members: list[dict], periods: list[int]) -> dict[int, float]:
    """Calculate retention rate at each day threshold."""
    total = len(members) or 1
    return {
        days: sum(1 for m in members if 0 <= m["days_inactive"] <= days) / total * 100
        for days in periods
    }


def get_activity_buckets(members: list[dict]) -> list[dict]:
    """Group members by inactivity period for histogram."""
    buckets = [
        (0, 7, "0-7d"),
        (8, 14, "8-14d"),
        (15, 30, "15-30d"),
        (31, 60, "31-60d"),
        (61, 90, "61-90d"),
        (91, 180, "91-180d"),
        (181, 365, "181-365d"),
        (366, 9999, "1y+"),
    ]
    
    total = len(members) or 1
    result = []
    
    for min_d, max_d, label in buckets:
        count = sum(1 for m in members if min_d <= m.get("days_inactive", 9999) <= max_d)
        result.append({
            "label": label,
            "count": count,
            "pct": count / total * 100,
        })
    
    return result
