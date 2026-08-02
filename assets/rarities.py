# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
Rarity System - All rarity definitions and mappings
"""

# ==========================================
# RARITY MAP - ID to Display Name with Emoji
# ==========================================

RARITY_MAP = {
    1: "⚪️ Common",
    2: "🟣 Rare",
    3: "🟢 Medium",
    4: "🟡 Legendary",
    5: "💮 Special Edition",
    6: "🔮 Limited Edition",
    7: "💸 Premium Edition",
    8: "🌤 Summer",
    9: "🎐 Enchanted",
    10: "❄️ Frozen",
    11: "💝 Romantic",
    12: "🎃 Haunted",
    13: "🎄 Christmas",
    14: "🧧 Festive",
    15: "🍑 Naughty",
    16: "🎗️ AMV Edition",
    17: "🌧 Cloudy",
    18: "🦠 Mythgard",
}


# ==========================================
# RARITY NAMES - List of all rarity names
# ==========================================

RARITY_NAMES = [
    "⚪️ Common",
    "🟣 Rare",
    "🟢 Medium",
    "🟡 Legendary",
    "💮 Special Edition",
    "🔮 Limited Edition",
    "💸 Premium Edition",
    "🌤 Summer",
    "🎐 Enchanted",
    "❄️ Frozen",
    "💝 Romantic",
    "🎃 Haunted",
    "🎄 Christmas",
    "🧧 Festive",
    "🍑 Naughty",
    "🎗️ AMV Edition",
    "🌧 Cloudy",
    "🦠 Mythgard",
]


# ==========================================
# RARITY EMOJI MAP - Display Name to Emoji
# ==========================================

RARITY_EMOJI_MAP = {
    "⚪️ Common": "⚪️",
    "🟣 Rare": "🟣",
    "🟢 Medium": "🟢",
    "🟡 Legendary": "🟡",
    "💮 Special Edition": "💮",
    "🔮 Limited Edition": "🔮",
    "💸 Premium Edition": "💸",
    "🌤 Summer": "🌤",
    "🎐 Enchanted": "🎐",
    "❄️ Frozen": "❄️",
    "💝 Romantic": "💝",
    "🎃 Haunted": "🎃",
    "🎄 Christmas": "🎄",
    "🧧 Festive": "🧧",
    "🍑 Naughty": "🍑",
    "🎗️ AMV Edition": "🎗️",
    "🌧 Cloudy": "🌧",
    "🦠 Mythgard": "🦠",
}


# ==========================================
# RARITY WEIGHTS - For random selection
# ==========================================

RARITY_WEIGHTS = {
    "⚪️ Common": 35,
    "🟣 Rare": 20,
    "🟢 Medium": 15,
    "🟡 Legendary": 12,
    "💮 Special Edition": 8,
    "🔮 Limited Edition": 6,
    "💸 Premium Edition": 4,
    "🌤 Summer": 3,
    "🎐 Enchanted": 2.5,
    "❄️ Frozen": 2,
    "💝 Romantic": 2,
    "🎃 Haunted": 1.8,
    "🎄 Christmas": 1.5,
    "🧧 Festive": 1.2,
    "🍑 Naughty": 1,
    "🎗️ AMV Edition": 0.8,
    "🌧 Cloudy": 0.6,
    "🦠 Mythgard": 0.5,
}


# ==========================================
# RARITY PRICES - For shop
# ==========================================

RARITY_PRICES = {
    "⚪️ Common": 1_000,
    "🟣 Rare": 5_000,
    "🟢 Medium": 15_000,
    "🟡 Legendary": 30_000,
    "💮 Special Edition": 50_000,
    "🔮 Limited Edition": 75_000,
    "💸 Premium Edition": 200_000,
    "🌤 Summer": 80_000,
    "🎐 Enchanted": 75_000,
    "❄️ Frozen": 80_000,
    "💝 Romantic": 85_000,
    "🎃 Haunted": 75_000,
    "🎄 Christmas": 70_000,
    "🧧 Festive": 100_000,
    "🍑 Naughty": 100_000,
    "🎗️ AMV Edition": 200_000,
    "🌧 Cloudy": 80_000,
    "🦠 Mythgard": 500_000,
}


# ==========================================
# RARITY DESCRIPTIONS - For shop display
# ==========================================

RARITY_DESCRIPTIONS = {
    "⚪️ Common": "A gentle spirit that blooms in every garden—simple, yet charming.",
    "🟣 Rare": "A butterfly with a delicate hue—not easily found, but worth the search.",
    "🟢 Medium": "Neither common nor rare—a balanced spirit with quiet strength.",
    "🟡 Legendary": "A soul that echoes through time—legendary tales are woven around them.",
    "💮 Special Edition": "A rare bloom that appears only during special seasons—cherish it.",
    "🔮 Limited Edition": "A treasure from beyond the veil—once it's gone, it's gone forever.",
    "💸 Premium Edition": "The crown jewel of the garden—only the most dedicated collectors may obtain this spirit.",
    "🌤 Summer": "A radiant spirit born from the summer sun's warm embrace.",
    "🎐 Enchanted": "A mystical being touched by ancient magic and wonder.",
    "❄️ Frozen": "A spirit preserved in eternal winter's icy beauty.",
    "💝 Romantic": "A soul filled with love and passion—perfect for Valentine's Day.",
    "🎃 Haunted": "A mysterious entity from the shadowy realm of Halloween.",
    "🎄 Christmas": "A festive spirit spreading joy and holiday cheer.",
    "🧧 Festive": "A celebration spirit that brings good fortune and happiness.",
    "🍑 Naughty": "A cheeky spirit with a mischievous glint in their eye.",
    "🎗️ AMV Edition": "A dynamic spirit full of energy and rhythm.",
    "🌧 Cloudy": "A melancholic spirit that brings gentle rain and reflection.",
    "🦠 Mythgard": "A legendary being from the mythical realms of old.",
}


# ==========================================
# RARITY ORDER - Display order
# ==========================================

RARITY_ORDER = [
    "⚪️ Common",
    "🟣 Rare",
    "🟢 Medium",
    "🟡 Legendary",
    "💮 Special Edition",
    "🔮 Limited Edition",
    "💸 Premium Edition",
    "🌤 Summer",
    "🎐 Enchanted",
    "❄️ Frozen",
    "💝 Romantic",
    "🎃 Haunted",
    "🎄 Christmas",
    "🧧 Festive",
    "🍑 Naughty",
    "🎗️ AMV Edition",
    "🌧 Cloudy",
    "🦠 Mythgard",
]


# ==========================================
# RARITY LIMITS (Default)
# ==========================================

DEFAULT_RARITY_LIMITS = {
    "⚪️ Common": 100,
    "🟣 Rare": 80,
    "🟢 Medium": 60,
    "🟡 Legendary": 40,
    "💮 Special Edition": 30,
    "🔮 Limited Edition": 25,
    "💸 Premium Edition": 20,
    "🌤 Summer": 15,
    "🎐 Enchanted": 12,
    "❄️ Frozen": 10,
    "💝 Romantic": 8,
    "🎃 Haunted": 6,
    "🎄 Christmas": 5,
    "🧧 Festive": 4,
    "🍑 Naughty": 3,
    "🎗️ AMV Edition": 2,
    "🌧 Cloudy": 2,
    "🦠 Mythgard": 1,
}


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def get_rarity_id(rarity_name: str) -> int:
    """Get rarity ID from name."""
    for rid, name in RARITY_MAP.items():
        if name == rarity_name:
            return rid
    return 1


def get_rarity_name(rarity_id: int) -> str:
    """Get rarity name from ID."""
    return RARITY_MAP.get(rarity_id, "⚪️ Common")


def get_rarity_emoji(rarity_name: str) -> str:
    """Get emoji from rarity name."""
    return RARITY_EMOJI_MAP.get(rarity_name, "🌸")


def get_rarity_weight(rarity_name: str) -> float:
    """Get weight from rarity name."""
    return RARITY_WEIGHTS.get(rarity_name, 1.0)


def get_rarity_price(rarity_name: str) -> int:
    """Get price from rarity name."""
    return RARITY_PRICES.get(rarity_name, 1000)


def get_rarity_description(rarity_name: str) -> str:
    """Get description from rarity name."""
    return RARITY_DESCRIPTIONS.get(rarity_name, "A beautiful spirit.")


def get_rarity_limit(rarity_name: str) -> int:
    """Get default limit from rarity name."""
    return DEFAULT_RARITY_LIMITS.get(rarity_name, 100)


def get_enabled_rarities() -> list:
    """Get all enabled rarities (excluding seasonal)."""
    return [
        "⚪️ Common", "🟣 Rare", "🟢 Medium", "🟡 Legendary",
        "💮 Special Edition", "🔮 Limited Edition", "💸 Premium Edition",
        "🎐 Enchanted", "🍑 Naughty", "🦠 Mythgard"
    ]


def get_seasonal_rarities() -> list:
    """Get all seasonal rarities."""
    return [
        "🌤 Summer", "❄️ Frozen", "💝 Romantic", "🎃 Haunted",
        "🎄 Christmas", "🧧 Festive", "🌧 Cloudy"
    ]


def get_special_rarities() -> list:
    """Get all special rarities."""
    return [
        "🎗️ AMV Edition"
    ]


def get_rarity_from_number(rarity_number: int) -> str:
    """Get rarity name from number (same as get_rarity_name)."""
    return get_rarity_name(rarity_number)


def get_number_from_rarity(rarity_name: str) -> int:
    """Get rarity number from name (same as get_rarity_id)."""
    return get_rarity_id(rarity_name)


# ==========================================
# LEGACY COMPATIBILITY (for old code)
# ==========================================

# Legacy variable names
rarity_map = RARITY_MAP
rarity_names = RARITY_NAMES
rarity_map2 = RARITY_EMOJI_MAP  # Display name to emoji
rarity_weights = RARITY_WEIGHTS
rarity_prices = RARITY_PRICES
rarity_descriptions = RARITY_DESCRIPTIONS
rarity_order = RARITY_ORDER
default_rarity_limits = DEFAULT_RARITY_LIMITS


__all__ = [
    'RARITY_MAP',
    'RARITY_NAMES',
    'RARITY_EMOJI_MAP',
    'RARITY_WEIGHTS',
    'RARITY_PRICES',
    'RARITY_DESCRIPTIONS',
    'RARITY_ORDER',
    'DEFAULT_RARITY_LIMITS',
    'get_rarity_id',
    'get_rarity_name',
    'get_rarity_emoji',
    'get_rarity_weight',
    'get_rarity_price',
    'get_rarity_description',
    'get_rarity_limit',
    'get_enabled_rarities',
    'get_seasonal_rarities',
    'get_special_rarities',
    'get_rarity_from_number',
    'get_number_from_rarity',
    # Legacy
    'rarity_map',
    'rarity_names',
    'rarity_map2',
    'rarity_weights',
    'rarity_prices',
    'rarity_descriptions',
    'rarity_order',
    'default_rarity_limits',
]
