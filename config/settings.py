"""Application settings for WOM Clan Tracker v2.0."""

APP_VERSION = "2.0.0"
APP_TITLE = "Clan Analytics Dashboard"
APP_ICON = "📊"

# WiseOldMan API
WOM_API_BASE = "https://api.wiseoldman.net/v2"
WOM_GROUP_ID = 11625
WOM_USER_AGENT = "Clan-Analytics-Dashboard/2.0"

# API Key is loaded from Streamlit secrets (never commit to repo!)
# See .streamlit/secrets.toml.example for format
# Per WOM docs: Use 1-6 hour intervals for auto-updates to avoid IP bans

# Cache TTLs (seconds)
CACHE_TTL_MEMBERS = 300      # 5 minutes for member list
CACHE_TTL_GAINS = 600        # 10 minutes for XP gains
CACHE_TTL_HISCORES = 300     # 5 minutes for hiscores
CACHE_TTL_DETAILS = 900      # 15 minutes for group details

# Activity classification thresholds (days)
ACTIVITY_THRESHOLDS = {
    "active": 7,        # Active if played within 7 days
    "at_risk": 30,      # At risk if 8-30 days inactive
    "inactive": 90,     # Inactive if 31-90 days
    "churned": 91,      # Churned if 90+ days
}

# Color scheme for activity status (modern palette)
ACTIVITY_COLORS = {
    "active": "#10b981",      # Emerald
    "at_risk": "#f59e0b",     # Amber
    "inactive": "#f97316",    # Orange
    "churned": "#ef4444",     # Red
    "unknown": "#6b7280",     # Gray
}

# Time period options for gains
GAIN_PERIODS = [
    "day",
    "week", 
    "month",
    "year",
]

DEFAULT_GAIN_PERIOD = "week"

# Skills list for OSRS
SKILLS = [
    "overall",
    "attack", "defence", "strength", "hitpoints", "ranged", "prayer",
    "magic", "cooking", "woodcutting", "fletching", "fishing",
    "firemaking", "crafting", "smithing", "mining", "herblore",
    "agility", "thieving", "slayer", "farming", "runecrafting",
    "hunter", "construction", "sailing",
]

COMBAT_SKILLS = ["attack", "defence", "strength", "hitpoints", "ranged", "prayer", "magic"]
