# ==========================================
# Admin Filters
# ==========================================

"""
Filters for admin and VIP users.
"""

from typing import Union

from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from app.core.config import Config
from app.services.permissions import PermissionService, Powers


class AdminOrVIPFilter(Filter):
    """
    Filter that allows only admin or VIP users.
    """
    
    async def __call__(
        self,
        event: Union[Message, CallbackQuery],
    ) -> bool:
        """
        Check if user is admin or VIP.
        
        Args:
            event: Message or CallbackQuery
            
        Returns:
            True if user is admin or VIP, False otherwise
        """
        from app.core.config import get_config
        from app.services.permissions import create_permission_service
        
        user = event.from_user
        if not user:
            return False
        
        config = get_config()
        permission_service = create_permission_service(config)
        
        return await permission_service.has_power(user.id, Powers.VIP)


class OwnerFilter(Filter):
    """
    Filter that allows only the bot owner.
    """
    
    async def __call__(
        self,
        event: Union[Message, CallbackQuery],
    ) -> bool:
        """
        Check if user is the bot owner.
        
        Args:
            event: Message or CallbackQuery
            
        Returns:
            True if user is owner, False otherwise
        """
        from app.core.config import get_config
        
        user = event.from_user
        if not user:
            return False
        
        config = get_config()
        return config.is_owner(user.id)
