# ==========================================
# Sudo User Repository
# ==========================================

from typing import Optional, List
from datetime import datetime

from app.database.manager import DatabaseManager
from app.database.models.sudo import SudoUser


class SudoUserRepository:
    """
    Repository for sudo user database operations.
    """
    
    COLLECTION = "sudo_users"
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize the repository.
        
        Args:
            db_manager: Database manager instance
        """
        self.db = db_manager
        self.collection = db_manager.get_collection(self.COLLECTION)
    
    async def get_by_user_id(self, user_id: int) -> Optional[SudoUser]:
        """
        Get a sudo user by user ID.
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            SudoUser if found, None otherwise
        """
        data = await self.collection.find_one({"_id": user_id})
        if data:
            return SudoUser.from_dict(data)
        return None
    
    async def save(self, sudo_user: SudoUser) -> None:
        """
        Save or update a sudo user.
        
        Args:
            sudo_user: SudoUser to save
        """
        sudo_user.updated_at = datetime.utcnow()
        await self.collection.update_one(
            {"_id": sudo_user.user_id},
            {"$set": sudo_user.to_dict()},
            upsert=True,
        )
    
    async def delete(self, user_id: int) -> bool:
        """
        Delete a sudo user.
        
        Args:
            user_id: User ID to delete
            
        Returns:
            True if deleted, False otherwise
        """
        result = await self.collection.delete_one({"_id": user_id})
        return result.deleted_count > 0
    
    async def get_all(self) -> List[SudoUser]:
        """
        Get all sudo users.
        
        Returns:
            List of SudoUser objects
        """
        cursor = self.collection.find()
        sudo_users = []
        async for data in cursor:
            sudo_users.append(SudoUser.from_dict(data))
        return sudo_users
    
    async def get_by_power(self, power: str) -> List[SudoUser]:
        """
        Get all users with a specific power.
        
        Args:
            power: Power name
            
        Returns:
            List of SudoUser objects
        """
        cursor = self.collection.find({"powers": power})
        sudo_users = []
        async for data in cursor:
            sudo_users.append(SudoUser.from_dict(data))
        return sudo_users
    
    async def create_indexes(self) -> None:
        """
        Create indexes for the collection.
        """
        await self.collection.create_index("_id", unique=True)
        await self.collection.create_index("powers")
        logger.info(f"✅ Indexes created for {self.COLLECTION}")
