"""Application configuration."""

# App metadata
APP_TITLE = "Clan Analytics"
APP_ICON = "⚔️"
APP_VERSION = "2.0.0"

# WiseOldMan API
# Docs: https://docs.wiseoldman.net/api
WOM_BASE_URL = "https://api.wiseoldman.net/v2"
WOM_USER_AGENT = "WOM-Clan-Dashboard/2.0"

# Default group - change this to your clan's group ID
# Find yours at: https://wiseoldman.net/groups
DEFAULT_GROUP_ID = 139  # Example group from WOM docs

# Cache TTLs (seconds)
CACHE_TTL_SHORT = 300   # 5 min - member data
CACHE_TTL_MEDIUM = 600  # 10 min - gains
CACHE_TTL_LONG = 900    # 15 min - group details

# Activity thresholds (days since last XP gain)
ACTIVITY_THRESHOLDS = {
    "active": 7,
    "at_risk": 30,
    "inactive": 90,
}

# Status colors
STATUS_COLORS = {
    "active": "#2ecc71",
    "at_risk": "#f1c40f",
    "inactive": "#e67e22",
    "churned": "#e74c3c",
    "unknown": "#95a5a6",
}

# Time periods for gains
PERIODS = ["day", "week", "month", "year"]
DEFAULT_PERIOD = "week"

# Skills list
SKILLS = [
    "overall", "attack", "defence", "strength", "hitpoints", "ranged",
    "prayer", "magic", "cooking", "woodcutting", "fletching", "fishing",
    "firemaking", "crafting", "smithing", "mining", "herblore", "agility",
    "thieving", "slayer", "farming", "runecrafting", "hunter", "construction",
]
