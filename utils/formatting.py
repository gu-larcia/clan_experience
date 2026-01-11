"""Formatting utilities."""

from datetime import datetime, timezone
from typing import Optional


def format_xp(value: float) -> str:
    """Format XP with K/M/B suffix."""
    if value is None:
        return "0"

    value = float(value)

    if value >= 1_000_000_000:
        return f"{value/1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"{value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"{value/1_000:.1f}K"
    else:
        return f"{int(value):,}"


def format_number(value: float, decimals: int = 0) -> str:
    """Format number with thousand separators."""
    if value is None:
        return "0"

    if decimals > 0:
        return f"{value:,.{decimals}f}"
    return f"{int(value):,}"


def format_hours(hours: float) -> str:
    """Format EHP/EHB hours."""
    if hours is None:
        return "0h"

    if hours >= 1000:
        return f"{hours/1000:.1f}K hrs"
    elif hours >= 1:
        return f"{hours:.1f} hrs"
    else:
        return f"{hours*60:.0f} min"


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format as percentage."""
    if value is None:
        return "0%"
    return f"{value:.{decimals}f}%"


def format_time_ago(dt: Optional[datetime]) -> str:
    """Format datetime as relative time."""
    if not dt:
        return "Never"

    now = datetime.now(timezone.utc)

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    delta = now - dt
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60

    if days > 365:
        years = days // 365
        return f"{years}y ago"
    elif days > 30:
        months = days // 30
        return f"{months}mo ago"
    elif days > 0:
        return f"{days}d ago"
    elif hours > 0:
        return f"{hours}h ago"
    elif minutes > 0:
        return f"{minutes}m ago"
    else:
        return "Just now"


def format_date(dt: Optional[datetime], include_time: bool = False) -> str:
    """Format datetime for display."""
    if not dt:
        return "N/A"

    if include_time:
        return dt.strftime("%b %d, %Y %H:%M")
    return dt.strftime("%b %d, %Y")


def truncate_username(username: str, max_length: int = 12) -> str:
    """Truncate long usernames."""
    if len(username) <= max_length:
        return username
    return username[:max_length-1] + "..."


def role_display_name(role: str) -> str:
    """Convert API role to display name."""
    role_map = {
        "owner": "Owner",
        "deputy_owner": "Deputy Owner",
        "administrator": "Admin",
        "moderator": "Moderator",
        "member": "Member",
        "recruit": "Recruit",
        "captain": "Captain",
        "general": "General",
        "lieutenant": "Lieutenant",
        "sergeant": "Sergeant",
        "corporal": "Corporal",
        "leader": "Leader",
        "coordinator": "Coordinator",
        "champion": "Champion",
        "legend": "Legend",
        "veteran": "Veteran",
        "elite": "Elite",
    }

    return role_map.get(role.lower(), role.replace("_", " ").title())
