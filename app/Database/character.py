# ==========================================
# Character Repository
# ==========================================

from typing import List, Optional, Pattern
import logging

from app.database.manager import DatabaseManager
from app.database.models.character import Character

logger = logging.getLogger(__name__)


class CharacterRepository:
    """
    Repository for character database operations.
    """
    
    COLLECTION = "anime_characters_lol"
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize the repository.
        
        Args:
            db_manager: Database manager instance
        """
        self.db = db_manager
        self.collection = db_manager.get_collection(self.COLLECTION)
    
    async def get_by_id(self, character_id: int) -> Optional[Character]:
        """
        Get a character by ID.
        
        Args:
            character_id: Character ID
            
        Returns:
            Character if found, None otherwise
        """
        data = await self.collection.find_one({"_id": character_id})
        if data:
            return Character.from_dict(data)
        return None
    
    async def get_by_name(self, name: str) -> List[Character]:
        """
        Get characters by name (exact match).
        
        Args:
            name: Character name
            
        Returns:
            List of matching characters
        """
        cursor = self.collection.find({"name": name})
        characters = []
        async for data in cursor:
            characters.append(Character.from_dict(data))
        return characters
    
    async def search(
        self,
        fields: List[str],
        pattern: Pattern,
        limit: int = 50,
        offset: int = 0
    ) -> List[Character]:
        """
        Search characters using regex pattern on specified fields.
        
        Args:
            fields: List of field names to search
            pattern: Regex pattern to match
            limit: Maximum number of results
            offset: Results offset
            
        Returns:
            List of matching characters
        """
        # Build OR query for multiple fields
        or_conditions = [{field: pattern} for field in fields]
        query = {"$or": or_conditions}
        
        cursor = self.collection.find(query)
        cursor = cursor.skip(offset).limit(limit)
        
        characters = []
        async for data in cursor:
            characters.append(Character.from_dict(data))
        return characters
    
    async def get_all(self, limit: Optional[int] = None) -> List[Character]:
        """
        Get all characters.
        
        Args:
            limit: Maximum number of characters to return
            
        Returns:
            List of all characters
        """
        cursor = self.collection.find()
        if limit:
            cursor = cursor.limit(limit)
        
        characters = []
        async for data in cursor:
            characters.append(Character.from_dict(data))
        return characters
    
    async def create(self, character: Character) -> None:
        """
        Create a new character.
        
        Args:
            character: Character to create
        """
        await self.collection.insert_one(character.to_dict())
        logger.info(f"Created character: {character.name} (ID: {character.id})")
    
    async def update(self, character: Character) -> None:
        """
        Update an existing character.
        
        Args:
            character: Character to update
        """
        character.updated_at = datetime.utcnow()
        await self.collection.update_one(
            {"_id": character.id},
            {"$set": character.to_dict()}
        )
        logger.info(f"Updated character: {character.name} (ID: {character.id})")
    
    async def delete(self, character_id: int) -> bool:
        """
        Delete a character.
        
        Args:
            character_id: Character ID to delete
            
        Returns:
            True if deleted, False otherwise
        """
        result = await self.collection.delete_one({"_id": character_id})
        if result.deleted_count > 0:
            logger.info(f"Deleted character ID: {character_id}")
            return True
        return False
    
    async def get_by_rarity(self, rarity: int) -> List[Character]:
        """
        Get characters by rarity level.
        
        Args:
            rarity: Rarity level
            
        Returns:
            List of characters with the given rarity
        """
        cursor = self.collection.find({"rarity": rarity})
        characters = []
        async for data in cursor:
            characters.append(Character.from_dict(data))
        return characters
    
    async def create_indexes(self) -> None:
        """
        Create indexes for the collection.
        """
        await self.collection.create_index("_id", unique=True)
        await self.collection.create_index("name")
        await self.collection.create_index("anime")
        await self.collection.create_index("rarity")
        await self.collection.create_index("aliases")
        await self.collection.create_index([("anime", 1), ("rarity", 1)])
        logger.info(f"✅ Indexes created for {self.COLLECTION}")
