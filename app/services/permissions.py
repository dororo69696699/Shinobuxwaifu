# ==========================================
# Permissions Service (Updated)
# ==========================================

"""
Updated permissions service with VIP check.
"""

import logging
from typing import List, Optional, Union

from app.core.config import Config
from app.database.repositories.sudo import SudoUserRepository
from app.database.models.sudo import SudoUser

logger = logging.getLogger(__name__)


# ===== Power Definitions =====
class Powers:
    """
    Available permission powers for sudo users.
    """
    ADD = "add"
    DELETE = "del"
    UPDATE = "up"
    APPROVE = "app"
    INVENTORY = "inv"
    VIP = "VIP"
    BAN = "ban"
    UNBAN = "unban"
    BROADCAST = "broadcast"
    STATS = "stats"
    BACKUP = "backup"
    SETTINGS = "settings"
    
    ALL = [ADD, DELETE, UPDATE, APPROVE, INVENTORY, VIP, BAN, UNBAN, 
           BROADCAST, STATS, BACKUP, SETTINGS]


class PermissionService:
    """
    Service for managing sudo user permissions.
    """
    
    def __init__(self, config: Config, sudo_repo: SudoUserRepository):
        self.config = config
        self.sudo_repo = sudo_repo
        self._cache = {}
    
    async def has_power(self, user_id: int, power: str) -> bool:
        """
        Check if a user has a specific power.
        
        Args:
            user_id: Telegram user ID
            power: Power name
            
        Returns:
            True if user has the power
        """
        # Owner has all powers
        if self.config.is_owner(user_id):
            return True
        
        # Check cache
        if user_id in self._cache:
            return self._cache[user_id].has_power(power)
        
        # Check database
        sudo_user = await self.sudo_repo.get_by_user_id(user_id)
        if sudo_user:
            self._cache[user_id] = sudo_user
            return sudo_user.has_power(power)
        
        return False
    
    async def is_vip_or_owner(self, user_id: int) -> bool:
        """
        Check if user is VIP or owner.
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            True if user is owner or has VIP power
        """
        return await self.has_power(user_id, Powers.VIP)
    
    # ... rest of the service methods
