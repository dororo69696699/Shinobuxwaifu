# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# Rewritten with Clean Architecture
# ==========================================

"""
Rarity System Module

Defines all rarity tiers with their:
- Numeric IDs
- Display names with emojis
- Emoji-only representation
- Weights for random selection
- Category (standard, seasonal, special)
"""

from typing import Dict, List, Optional, Tuple
from enum import IntEnum
from dataclasses import dataclass, field


class RarityID(IntEnum):
    """
    Numeric IDs for each rarity tier.
    """
    COMMON = 1
    RARE = 2
    MEDIUM = 3
    LEGENDARY = 4
    SPECIAL_EDITION = 5
    LIMITED_EDITION = 6
    PREMIUM_EDITION = 7
    SUMMER = 8
    ENCHANTED = 9
    FROZEN = 10
    ROMANTIC = 11
    HAUNTED = 12
    CHRISTMAS = 13
    FESTIVE = 14
    NAUGHTY = 15
    AMV_EDITION = 16
    CLOUDY = 17
    MYTHGARD = 18


@dataclass
class Rarity:
    """
    Represents a single rarity tier.
    """
    id: int
    name: str
    emoji: str
    display_name: str
    weight: float = 1.0
    category: str = "standard"
    enabled: bool = True
    
    def get_emoji_only(self) -> str:
        """
        Get just the emoji for this rarity.
        
        Returns:
            Emoji string
        """
        return self.emoji
    
    def get_display(self) -> str:
        """
        Get the full display name with emoji.
        
        Returns:
            Display name (e.g., "⚪️ Common")
        """
        return self.display_name
    
    def to_dict(self) -> Dict[str, any]:
        """
        Convert to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            "id": self.id,
            "name": self.name,
            "emoji": self.emoji,
            "display_name": self.display_name,
            "weight": self.weight,
            "category": self.category,
            "enabled": self.enabled,
        }


class RaritySystem:
    """
    Centralized rarity management system.
    """
    
    # Internal rarity definitions
    _RARITIES = {
        RarityID.COMMON: Rarity(
            id=1,
            name="Common",
            emoji="⚪️",
            display_name="⚪️ Common",
            weight=35.0,
            category="standard",
            enabled=True,
        ),
        RarityID.RARE: Rarity(
            id=2,
            name="Rare",
            emoji="🟣",
            display_name="🟣 Rare",
            weight=20.0,
            category="standard",
            enabled=True,
        ),
        RarityID.MEDIUM: Rarity(
            id=3,
            name="Medium",
            emoji="🟢",
            display_name="🟢 Medium",
            weight=15.0,
            category="standard",
            enabled=True,
        ),
        RarityID.LEGENDARY: Rarity(
            id=4,
            name="Legendary",
            emoji="🟡",
            display_name="🟡 Legendary",
            weight=12.0,
            category="standard",
            enabled=True,
        ),
        RarityID.SPECIAL_EDITION: Rarity(
            id=5,
            name="Special Edition",
            emoji="💮",
            display_name="💮 Special Edition",
            weight=8.0,
            category="special",
            enabled=True,
        ),
        RarityID.LIMITED_EDITION: Rarity(
            id=6,
            name="Limited Edition",
            emoji="🔮",
            display_name="🔮 Limited Edition",
            weight=6.0,
            category="special",
            enabled=True,
        ),
        RarityID.PREMIUM_EDITION: Rarity(
            id=7,
            name="Premium Edition",
            emoji="💸",
            display_name="💸 Premium Edition",
            weight=4.0,
            category="special",
            enabled=True,
        ),
        RarityID.SUMMER: Rarity(
            id=8,
            name="Summer",
            emoji="🌤",
            display_name="🌤 Summer",
            weight=3.0,
            category="seasonal",
            enabled=False,
        ),
        RarityID.ENCHANTED: Rarity(
            id=9,
            name="Enchanted",
            emoji="🎐",
            display_name="🎐 Enchanted",
            weight=2.5,
            category="special",
            enabled=True,
        ),
        RarityID.FROZEN: Rarity(
            id=10,
            name="Frozen",
            emoji="❄️",
            display_name="❄️ Frozen",
            weight=2.0,
            category="seasonal",
            enabled=False,
        ),
        RarityID.ROMANTIC: Rarity(
            id=11,
            name="Romantic",
            emoji="💝",
            display_name="💝 Romantic",
            weight=2.0,
            category="seasonal",
            enabled=False,
        ),
        RarityID.HAUNTED: Rarity(
            id=12,
            name="Haunted",
            emoji="🎃",
            display_name="🎃 Haunted",
            weight=1.8,
            category="seasonal",
            enabled=False,
        ),
        RarityID.CHRISTMAS: Rarity(
            id=13,
            name="Christmas",
            emoji="🎄",
            display_name="🎄 Christmas",
            weight=1.5,
            category="seasonal",
            enabled=False,
        ),
        RarityID.FESTIVE: Rarity(
            id=14,
            name="Festive",
            emoji="🧧",
            display_name="🧧 Festive",
            weight=1.2,
            category="seasonal",
            enabled=False,
        ),
        RarityID.NAUGHTY: Rarity(
            id=15,
            name="Naughty",
            emoji="🍑",
            display_name="🍑 Naughty",
            weight=1.0,
            category="special",
            enabled=True,
        ),
        RarityID.AMV_EDITION: Rarity(
            id=16,
            name="AMV Edition",
            emoji="🎗️",
            display_name="🎗️ AMV Edition",
            weight=0.8,
            category="special",
            enabled=False,
        ),
        RarityID.CLOUDY: Rarity(
            id=17,
            name="Cloudy",
            emoji="🌧",
            display_name="🌧 Cloudy",
            weight=0.6,
            category="seasonal",
            enabled=False,
        ),
        RarityID.MYTHGARD: Rarity(
            id=18,
            name="Mythgard",
            emoji="🦠",
            display_name="🦠 Mythgard",
            weight=0.5,
            category="special",
            enabled=True,
        ),
    }
    
    @classmethod
    def get_all(cls) -> List[Rarity]:
        """
        Get all rarities.
        
        Returns:
            List of all Rarity objects
        """
        return list(cls._RARITIES.values())
    
    @classmethod
    def get_by_id(cls, rarity_id: int) -> Optional[Rarity]:
        """
        Get a rarity by its numeric ID.
        
        Args:
            rarity_id: Numeric ID of the rarity
            
        Returns:
            Rarity object if found, None otherwise
        """
        return cls._RARITIES.get(rarity_id)
    
    @classmethod
    def get_by_name(cls, name: str) -> Optional[Rarity]:
        """
        Get a rarity by its name (case-insensitive).
        
        Args:
            name: Name of the rarity
            
        Returns:
            Rarity object if found, None otherwise
        """
        name_lower = name.lower()
        for rarity in cls._RARITIES.values():
            if rarity.name.lower() == name_lower:
                return rarity
        return None
    
    @classmethod
    def get_by_display_name(cls, display_name: str) -> Optional[Rarity]:
        """
        Get a rarity by its display name (with emoji).
        
        Args:
            display_name: Display name (e.g., "⚪️ Common")
            
        Returns:
            Rarity object if found, None otherwise
        """
        for rarity in cls._RARITIES.values():
            if rarity.display_name == display_name:
                return rarity
        return None
    
    @classmethod
    def get_id_by_display_name(cls, display_name: str) -> Optional[int]:
        """
        Get the numeric ID from a display name.
        
        Args:
            display_name: Display name (e.g., "⚪️ Common")
            
        Returns:
            Numeric ID if found, None otherwise
        """
        rarity = cls.get_by_display_name(display_name)
        return rarity.id if rarity else None
    
    @classmethod
    def get_emoji_by_id(cls, rarity_id: int) -> Optional[str]:
        """
        Get the emoji for a rarity ID.
        
        Args:
            rarity_id: Numeric ID
            
        Returns:
            Emoji string if found, None otherwise
        """
        rarity = cls.get_by_id(rarity_id)
        return rarity.emoji if rarity else None
    
    @classmethod
    def get_emoji_by_name(cls, name: str) -> Optional[str]:
        """
        Get the emoji for a rarity name.
        
        Args:
            name: Rarity name
            
        Returns:
            Emoji string if found, None otherwise
        """
        rarity = cls.get_by_name(name)
        return rarity.emoji if rarity else None
    
    @classmethod
    def get_display_name_by_id(cls, rarity_id: int) -> Optional[str]:
        """
        Get the display name for a rarity ID.
        
        Args:
            rarity_id: Numeric ID
            
        Returns:
            Display name if found, None otherwise
        """
        rarity = cls.get_by_id(rarity_id)
        return rarity.display_name if rarity else None
    
    @classmethod
    def get_enabled(cls) -> List[Rarity]:
        """
        Get all enabled rarities.
        
        Returns:
            List of enabled Rarity objects
        """
        return [r for r in cls._RARITIES.values() if r.enabled]
    
    @classmethod
    def get_by_category(cls, category: str) -> List[Rarity]:
        """
        Get rarities by category.
        
        Args:
            category: Category name ('standard', 'special', 'seasonal')
            
        Returns:
            List of Rarity objects in the category
        """
        return [r for r in cls._RARITIES.values() if r.category == category]
    
    @classmethod
    def get_display_names(cls) -> List[str]:
        """
        Get all display names.
        
        Returns:
            List of display names
        """
        return [r.display_name for r in cls._RARITIES.values()]
    
    @classmethod
    def get_enabled_display_names(cls) -> List[str]:
        """
        Get all enabled display names.
        
        Returns:
            List of enabled display names
        """
        return [r.display_name for r in cls.get_enabled()]
    
    @classmethod
    def get_ids(cls) -> List[int]:
        """
        Get all numeric IDs.
        
        Returns:
            List of numeric IDs
        """
        return list(cls._RARITIES.keys())
    
    @classmethod
    def get_emoji_only(cls, display_name: str) -> str:
        """
        Get just the emoji from a display name.
        
        Args:
            display_name: Display name (e.g., "⚪️ Common")
            
        Returns:
            Emoji string (e.g., "⚪️")
        """
        rarity = cls.get_by_display_name(display_name)
        return rarity.emoji if rarity else ""
    
    @classmethod
    def get_weight(cls, display_name: str) -> float:
        """
        Get the weight for a rarity.
        
        Args:
            display_name: Display name
            
        Returns:
            Weight value, defaults to 0 if not found
        """
        rarity = cls.get_by_display_name(display_name)
        return rarity.weight if rarity else 0.0
    
    @classmethod
    def get_rarity_by_display_name(cls, display_name: str) -> Optional[Dict]:
        """
        Get full rarity data by display name (legacy format).
        
        Args:
            display_name: Display name
            
        Returns:
            Dictionary with rarity data or None
        """
        rarity = cls.get_by_display_name(display_name)
        if rarity:
            return rarity.to_dict()
        return None
    
    @classmethod
    def get_all_display_names_with_emojis(cls) -> Dict[str, str]:
        """
        Get mapping of display names to emojis (legacy rarity_map2).
        
        Returns:
            Dict mapping display name to emoji
        """
        return {
            r.display_name: r.emoji
            for r in cls._RARITIES.values()
        }
    
    @classmethod
    def get_id_to_display_name_map(cls) -> Dict[int, str]:
        """
        Get mapping of IDs to display names (legacy rarity_map).
        
        Returns:
            Dict mapping ID to display name
        """
        return {
            r.id: r.display_name
            for r in cls._RARITIES.values()
        }


# ===== Backward Compatibility =====

# Legacy rarity_map - maps ID to display name
rarity_map: Dict[int, str] = RaritySystem.get_id_to_display_name_map()

# Legacy RARITY_NAMES - list of all display names
RARITY_NAMES: List[str] = RaritySystem.get_display_names()

# Legacy rarity_map2 - maps display name to emoji
rarity_map2: Dict[str, str] = RaritySystem.get_all_display_names_with_emojis()

# Also export the Rarity class for use in other modules
__all__ = [
    "Rarity",
    "RarityID",
    "RaritySystem",
    "rarity_map",
    "RARITY_NAMES",
    "rarity_map2",
]
