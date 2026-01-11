"""Application configuration constants."""

APP_VERSION = "2.0.0"
APP_TITLE = "Clan Analytics Dashboard"
APP_ICON = ""  # No icon

# WiseOldMan API
WOM_API_BASE = "https://api.wiseoldman.net/v2"
WOM_GROUP_ID = 11625
WOM_USER_AGENT = "Clan-Analytics-Dashboard/2.0"

# Cache TTLs in seconds
CACHE_TTL_MEMBERS = 300      # 5 min
CACHE_TTL_GAINS = 600        # 10 min
CACHE_TTL_HISCORES = 300     # 5 min
CACHE_TTL_DETAILS = 900      # 15 min

# Activity classification thresholds in days
ACTIVITY_THRESHOLDS = {
    "active": 7,
    "at_risk": 30,
    "inactive": 90,
    "churned": 91,
}

# Status colors
ACTIVITY_COLORS = {
    "active": "#10b981",
    "at_risk": "#f59e0b",
    "inactive": "#f97316",
    "churned": "#ef4444",
    "unknown": "#6b7280",
}

# Gain period options
GAIN_PERIODS = ["day", "week", "month", "year"]
DEFAULT_GAIN_PERIOD = "week"

# OSRS skills
SKILLS = [
    "overall",
    "attack", "defence", "strength", "hitpoints", "ranged", "prayer",
    "magic", "cooking", "woodcutting", "fletching", "fishing",
    "firemaking", "crafting", "smithing", "mining", "herblore",
    "agility", "thieving", "slayer", "farming", "runecrafting",
    "hunter", "construction", "sailing",
]

COMBAT_SKILLS = [
    "attack", "defence", "strength", "hitpoints", "ranged", "prayer", "magic"
]
