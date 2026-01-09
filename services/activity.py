"""Activity analysis and churn classification service."""

from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class ActivityStatus:
    """Player activity classification."""
    status: str          # active, at_risk, inactive, churned
    days_inactive: int
    last_activity: Optional[datetime]
    color: str
    description: str


def classify_activity(
    last_changed_at: Optional[datetime],
    thresholds: Dict[str, int],
    colors: Dict[str, str]
) -> ActivityStatus:
    """
    Classify player activity based on last XP gain.
    
    Args:
        last_changed_at: Datetime of last recorded XP change
        thresholds: Dict with 'active', 'at_risk', 'inactive', 'churned' day counts
        colors: Dict mapping status to color hex codes
        
    Returns:
        ActivityStatus with classification details
    """
    if not last_changed_at:
        return ActivityStatus(
            status="unknown",
            days_inactive=-1,
            last_activity=None,
            color=colors.get("unknown", "#95a5a6"),
            description="No activity data"
        )
    
    now = datetime.now(timezone.utc)
    
    # Ensure last_changed_at is timezone-aware
    if last_changed_at.tzinfo is None:
        last_changed_at = last_changed_at.replace(tzinfo=timezone.utc)
    
    days_inactive = (now - last_changed_at).days
    
    if days_inactive <= thresholds["active"]:
        status = "active"
        description = f"Active ({days_inactive}d ago)"
    elif days_inactive <= thresholds["at_risk"]:
        status = "at_risk"
        description = f"At risk ({days_inactive}d inactive)"
    elif days_inactive <= thresholds["inactive"]:
        status = "inactive"
        description = f"Inactive ({days_inactive}d)"
    else:
        status = "churned"
        description = f"Churned ({days_inactive}d)"
    
    return ActivityStatus(
        status=status,
        days_inactive=days_inactive,
        last_activity=last_changed_at,
        color=colors.get(status, "#95a5a6"),
        description=description
    )


def analyze_clan_activity(
    members: List[Dict],
    thresholds: Dict[str, int],
    colors: Dict[str, str]
) -> Dict:
    """
    Analyze activity patterns across entire clan.
    
    Args:
        members: List of member dicts from WOM API
        thresholds: Activity thresholds
        colors: Status colors
        
    Returns:
        Dict with counts, percentages, and member classifications
    """
    from .api import parse_wom_datetime
    
    classifications = []
    status_counts = {
        "active": 0,
        "at_risk": 0, 
        "inactive": 0,
        "churned": 0,
        "unknown": 0
    }
    
    total_xp = 0
    total_ehp = 0
    total_ehb = 0
    
    for member in members:
        player = member.get("player", {})
        membership = member.get("membership", {})
        
        # Parse last activity timestamp
        last_changed = parse_wom_datetime(player.get("lastChangedAt"))
        
        # Classify activity
        activity = classify_activity(last_changed, thresholds, colors)
        status_counts[activity.status] += 1
        
        # Aggregate stats
        total_xp += player.get("exp", 0) or 0
        total_ehp += player.get("ehp", 0) or 0
        total_ehb += player.get("ehb", 0) or 0
        
        classifications.append({
            "username": player.get("displayName", player.get("username", "Unknown")),
            "player_id": player.get("id"),
            "role": membership.get("role", "member"),
            "exp": player.get("exp", 0),
            "ehp": player.get("ehp", 0),
            "ehb": player.get("ehb", 0),
            "type": player.get("type", "regular"),
            "build": player.get("build", "main"),
            "last_changed_at": last_changed,
            "activity_status": activity.status,
            "days_inactive": activity.days_inactive,
            "status_color": activity.color,
            "status_description": activity.description,
            "joined_at": parse_wom_datetime(membership.get("createdAt")),
        })
    
    total_members = len(members)
    
    return {
        "total_members": total_members,
        "status_counts": status_counts,
        "status_percentages": {
            k: (v / total_members * 100) if total_members > 0 else 0
            for k, v in status_counts.items()
        },
        "total_xp": total_xp,
        "total_ehp": total_ehp,
        "total_ehb": total_ehb,
        "avg_xp": total_xp / total_members if total_members > 0 else 0,
        "avg_ehp": total_ehp / total_members if total_members > 0 else 0,
        "avg_ehb": total_ehb / total_members if total_members > 0 else 0,
        "members": classifications,
        "health_score": calculate_health_score(status_counts, total_members),
    }


def calculate_health_score(status_counts: Dict[str, int], total: int) -> float:
    """
    Calculate overall clan health score (0-100).
    
    Weights:
    - Active: 100 points
    - At Risk: 50 points  
    - Inactive: 20 points
    - Churned: 0 points
    """
    if total == 0:
        return 0.0
    
    weights = {
        "active": 100,
        "at_risk": 50,
        "inactive": 20,
        "churned": 0,
        "unknown": 25,
    }
    
    score = sum(
        status_counts.get(status, 0) * weight
        for status, weight in weights.items()
    )
    
    return score / total


def get_churn_risk_members(
    members: List[Dict],
    min_days: int = 14,
    max_days: int = 60
) -> List[Dict]:
    """
    Get members who are at risk of churning (intervention candidates).
    
    Args:
        members: Classified member list
        min_days: Minimum days inactive to be considered at risk
        max_days: Maximum days (beyond this they're already churned)
        
    Returns:
        List of at-risk members sorted by days inactive
    """
    at_risk = [
        m for m in members
        if min_days <= m.get("days_inactive", 0) <= max_days
    ]
    
    return sorted(at_risk, key=lambda x: x.get("days_inactive", 0), reverse=True)


def calculate_retention_rates(
    members: List[Dict],
    periods: List[int] = [7, 30, 90]
) -> Dict[int, float]:
    """
    Calculate retention rates at different day thresholds.
    
    Returns: {7: 85.2, 30: 72.1, 90: 58.4} (percentages)
    """
    total = len(members)
    if total == 0:
        return {p: 0.0 for p in periods}
    
    return {
        days: sum(
            1 for m in members 
            if m.get("days_inactive", 999) <= days
        ) / total * 100
        for days in periods
    }


def group_by_role(members: List[Dict]) -> Dict[str, List[Dict]]:
    """Group members by their clan role."""
    roles = {}
    for member in members:
        role = member.get("role", "member")
        if role not in roles:
            roles[role] = []
        roles[role].append(member)
    return roles


def get_activity_timeline(
    members: List[Dict],
    bucket_days: int = 7
) -> List[Dict]:
    """
    Create timeline buckets of when members were last active.
    
    Returns list of: {bucket: "0-7 days", count: 45, percentage: 32.1}
    """
    buckets = [
        (0, 7, "0-7 days"),
        (8, 14, "8-14 days"),
        (15, 30, "15-30 days"),
        (31, 60, "31-60 days"),
        (61, 90, "61-90 days"),
        (91, 180, "91-180 days"),
        (181, 365, "181-365 days"),
        (366, 9999, "1+ year"),
    ]
    
    total = len(members)
    timeline = []
    
    for min_d, max_d, label in buckets:
        count = sum(
            1 for m in members
            if min_d <= m.get("days_inactive", 9999) <= max_d
        )
        timeline.append({
            "bucket": label,
            "min_days": min_d,
            "max_days": max_d,
            "count": count,
            "percentage": (count / total * 100) if total > 0 else 0
        })
    
    return timeline
