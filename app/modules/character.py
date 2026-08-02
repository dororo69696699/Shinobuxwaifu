# ==========================================
# Character Model
# ==========================================

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class Character:
    """
    Model representing an anime character.
    """
    id: int
    name: str
    anime: str
    rarity: int
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    aliases: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    RARITY_NAMES = {
        0: "Common",
        1: "Medium",
        2: "Rare",
        3: "Legendary",
        4: "Celestial",
    }
    
    def get_rarity_name(self) -> str:
        """
        Get the human-readable rarity name.
        
        Returns:
            Rarity name
        """
        return self.RARITY_NAMES.get(self.rarity, "Unknown")
    
    def to_dict(self) -> dict:
        """
        Convert to dictionary for MongoDB storage.
        
        Returns:
            Dictionary representation
        """
        return {
            "_id": self.id,
            "name": self.name,
            "anime": self.anime,
            "rarity": self.rarity,
            "image_url": self.image_url,
            "video_url": self.video_url,
            "aliases": self.aliases,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Character":
        """
        Create from dictionary.
        
        Args:
            data: Dictionary from MongoDB
            
        Returns:
            Character instance
        """
        return cls(
            id=data.get("_id", 0),
            name=data.get("name", ""),
            anime=data.get("anime", ""),
            rarity=data.get("rarity", 0),
            image_url=data.get("image_url"),
            video_url=data.get("video_url"),
            aliases=data.get("aliases", []),
            created_at=data.get("created_at", datetime.utcnow()),
            updated_at=data.get("updated_at", datetime.utcnow()),
)
