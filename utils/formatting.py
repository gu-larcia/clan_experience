"""Formatting utilities for display."""

from datetime import datetime, timezone
from typing import Optional


def format_xp(value: float) -> str:
    """Format XP value with K/M/B suffix."""
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
    """Format EHP/EHB hours nicely."""
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
    """Format datetime as relative time string."""
    if not dt:
        return "Never"
    
    now = datetime.now(timezone.utc)
    
    # Ensure dt is timezone-aware
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


def get_skill_icon_url(skill_name: str) -> str:
    """Get OSRS Wiki icon URL for a skill."""
    # Handle special cases
    name_map = {
        "overall": "Stats",
        "hitpoints": "Hitpoints",
    }
    
    display_name = name_map.get(skill_name.lower(), skill_name.capitalize())
    formatted = display_name.replace(" ", "_")
    
    return f"https://oldschool.runescape.wiki/images/{formatted}_icon.png"


def get_player_avatar_url(username: str) -> str:
    """Generate a URL for player avatar (uses WOM's image proxy)."""
    # WOM doesn't provide avatars directly, but we can use a placeholder
    # or link to their profile
    return f"https://wiseoldman.net/players/{username}"


def truncate_username(username: str, max_length: int = 12) -> str:
    """Truncate long usernames with ellipsis."""
    if len(username) <= max_length:
        return username
    return username[:max_length-1] + "…"


def role_display_name(role: str) -> str:
    """Convert API role to display name."""
    role_map = {
        "achiever": "Achiever",
        "adamant": "Adamant",
        "adept": "Adept",
        "administrator": "Admin",
        "admiral": "Admiral",
        "adventurer": "Adventurer",
        "air": "Air",
        "anchor": "Anchor",
        "apothecary": "Apothecary",
        "archer": "Archer",
        "armadylean": "Armadylean",
        "artillery": "Artillery",
        "artisan": "Artisan",
        "asgarnian": "Asgarnian",
        "assistant": "Assistant",
        "astral": "Astral",
        "athlete": "Athlete",
        "attacker": "Attacker",
        "bandit": "Bandit",
        "bandosian": "Bandosian",
        "barbarian": "Barbarian",
        "battlemage": "Battlemage",
        "beast": "Beast",
        "berserker": "Berserker",
        "blisterwood": "Blisterwood",
        "blood": "Blood",
        "blue": "Blue",
        "bob": "Bob",
        "body": "Body",
        "brassican": "Brassican",
        "brawler": "Brawler",
        "brigadier": "Brigadier",
        "bronze": "Bronze",
        "bruiser": "Bruiser",
        "bulwark": "Bulwark",
        "burglar": "Burglar",
        "burnt": "Burnt",
        "cadet": "Cadet",
        "captain": "Captain",
        "carry": "Carry",
        "champion": "Champion",
        "chaos": "Chaos",
        "cleric": "Cleric",
        "collector": "Collector",
        "colonel": "Colonel",
        "commander": "Commander",
        "competitor": "Competitor",
        "completionist": "Completionist",
        "constructor": "Constructor",
        "cook": "Cook",
        "coordinator": "Coordinator",
        "corporal": "Corporal",
        "cosmic": "Cosmic",
        "councillor": "Councillor",
        "crafter": "Crafter",
        "crew": "Crew",
        "crusader": "Crusader",
        "cutpurse": "Cutpurse",
        "death": "Death",
        "defender": "Defender",
        "defiler": "Defiler",
        "deputy_owner": "Deputy Owner",
        "destroyer": "Destroyer",
        "diamond": "Diamond",
        "diseased": "Diseased",
        "doctor": "Doctor",
        "dogsbody": "Dogsbody",
        "dragon": "Dragon",
        "dragonstone": "Dragonstone",
        "druid": "Druid",
        "duellist": "Duellist",
        "earth": "Earth",
        "elite": "Elite",
        "emerald": "Emerald",
        "enforcer": "Enforcer",
        "epic": "Epic",
        "executive": "Executive",
        "expert": "Expert",
        "explorer": "Explorer",
        "farmer": "Farmer",
        "feeder": "Feeder",
        "fighter": "Fighter",
        "fire": "Fire",
        "firemaker": "Firemaker",
        "firestarter": "Firestarter",
        "fisher": "Fisher",
        "fletcher": "Fletcher",
        "forager": "Forager",
        "fremennik": "Fremennik",
        "gamer": "Gamer",
        "gatherer": "Gatherer",
        "general": "General",
        "gnome_child": "Gnome Child",
        "gnome_elder": "Gnome Elder",
        "goblin": "Goblin",
        "gold": "Gold",
        "goon": "Goon",
        "green": "Green",
        "grey": "Grey",
        "guardian": "Guardian",
        "guthixian": "Guthixian",
        "harpoon": "Harpoon",
        "healer": "Healer",
        "hellcat": "Hellcat",
        "helper": "Helper",
        "herbologist": "Herbologist",
        "hero": "Hero",
        "holy": "Holy",
        "hoarder": "Hoarder",
        "hunter": "Hunter",
        "ignitor": "Ignitor",
        "illusionist": "Illusionist",
        "imp": "Imp",
        "infantry": "Infantry",
        "inquisitor": "Inquisitor",
        "iron": "Iron",
        "jade": "Jade",
        "justiciar": "Justiciar",
        "kandarin": "Kandarin",
        "karamjan": "Karamjan",
        "kharidian": "Kharidian",
        "kitten": "Kitten",
        "knight": "Knight",
        "labourer": "Labourer",
        "law": "Law",
        "leader": "Leader",
        "learner": "Learner",
        "legacy": "Legacy",
        "legend": "Legend",
        "legionnaire": "Legionnaire",
        "lieutenant": "Lieutenant",
        "looter": "Looter",
        "lumberjack": "Lumberjack",
        "magic": "Magic",
        "magician": "Magician",
        "major": "Major",
        "maple": "Maple",
        "marshal": "Marshal",
        "master": "Master",
        "maxed": "Maxed",
        "mediator": "Mediator",
        "medic": "Medic",
        "member": "Member",
        "merchant": "Merchant",
        "mind": "Mind",
        "miner": "Miner",
        "minion": "Minion",
        "misthalinian": "Misthalinian",
        "mithril": "Mithril",
        "moderator": "Moderator",
        "monarch": "Monarch",
        "morytanian": "Morytanian",
        "mystic": "Mystic",
        "myth": "Myth",
        "natural": "Natural",
        "nature": "Nature",
        "necromancer": "Necromancer",
        "ninja": "Ninja",
        "noble": "Noble",
        "novice": "Novice",
        "nurse": "Nurse",
        "oak": "Oak",
        "officer": "Officer",
        "onyx": "Onyx",
        "opal": "Opal",
        "oracle": "Oracle",
        "orange": "Orange",
        "owner": "Owner",
        "page": "Page",
        "paladin": "Paladin",
        "pawn": "Pawn",
        "pilgrim": "Pilgrim",
        "pine": "Pine",
        "pink": "Pink",
        "prefect": "Prefect",
        "priest": "Priest",
        "private": "Private",
        "prodigy": "Prodigy",
        "proselyte": "Proselyte",
        "prospector": "Prospector",
        "protector": "Protector",
        "pure": "Pure",
        "purple": "Purple",
        "pyromancer": "Pyromancer",
        "quester": "Quester",
        "raider": "Raider",
        "ranger": "Ranger",
        "record_chaser": "Record Chaser",
        "recruit": "Recruit",
        "recruiter": "Recruiter",
        "red_topaz": "Red Topaz",
        "red": "Red",
        "rogue": "Rogue",
        "ruby": "Ruby",
        "rune": "Rune",
        "runecrafter": "Runecrafter",
        "sage": "Sage",
        "sapphire": "Sapphire",
        "saradominist": "Saradominist",
        "saviour": "Saviour",
        "scavenger": "Scavenger",
        "scholar": "Scholar",
        "scourge": "Scourge",
        "scout": "Scout",
        "scribe": "Scribe",
        "seer": "Seer",
        "senator": "Senator",
        "sentry": "Sentry",
        "serenist": "Serenist",
        "sergeant": "Sergeant",
        "shaman": "Shaman",
        "sheriff": "Sheriff",
        "short_green_guy": "Short Green Guy",
        "skiller": "Skiller",
        "skulled": "Skulled",
        "slayer": "Slayer",
        "smiter": "Smiter",
        "smith": "Smith",
        "smuggler": "Smuggler",
        "sniper": "Sniper",
        "soul": "Soul",
        "specialist": "Specialist",
        "speed_runner": "Speed Runner",
        "spellcaster": "Spellcaster",
        "squire": "Squire",
        "staff": "Staff",
        "steel": "Steel",
        "strider": "Strider",
        "striker": "Striker",
        "summoner": "Summoner",
        "superior": "Superior",
        "supervisor": "Supervisor",
        "teacher": "Teacher",
        "templar": "Templar",
        "therapist": "Therapist",
        "thief": "Thief",
        "tirannian": "Tirannian",
        "trialist": "Trialist",
        "trickster": "Trickster",
        "tzkal": "TzKal",
        "tztok": "TzTok",
        "unholy": "Unholy",
        "vagrant": "Vagrant",
        "vanguard": "Vanguard",
        "walker": "Walker",
        "wanderer": "Wanderer",
        "warden": "Warden",
        "warlock": "Warlock",
        "warrior": "Warrior",
        "water": "Water",
        "wild": "Wild",
        "willow": "Willow",
        "wily": "Wily",
        "wintumber": "Wintumber",
        "witch": "Witch",
        "wizard": "Wizard",
        "worker": "Worker",
        "wrath": "Wrath",
        "xerician": "Xerician",
        "yellow": "Yellow",
        "yew": "Yew",
        "zamorakian": "Zamorakian",
        "zarosian": "Zarosian",
        "zealot": "Zealot",
        "zenyte": "Zenyte",
    }
    
    return role_map.get(role.lower(), role.replace("_", " ").title())
