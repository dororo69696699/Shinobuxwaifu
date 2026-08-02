# ==========================================
# Cooldown Manager
# ==========================================

"""
Cooldown management for commands to prevent spam.
"""

import time
from typing import Dict, Optional


class CooldownManager:
    """
    Manages cooldowns for user commands.
    """
    
    def __init__(self, default_delay: int = 2):
        """
        Initialize the cooldown manager.
        
        Args:
            default_delay: Default cooldown delay in seconds
        """
        self.default_delay = default_delay
        self._cooldowns: Dict[str, float] = {}
    
    def check(self, user_id: int, command: str, delay: Optional[int] = None) -> bool:
        """
        Check if a user can execute a command.
        
        Args:
            user_id: User ID
            command: Command name
            delay: Optional custom delay
            
        Returns:
            True if allowed, False if on cooldown
        """
        delay = delay or self.default_delay
        key = f"{user_id}:{command}"
        
        now = time.time()
        if key in self._cooldowns:
            if now - self._cooldowns[key] < delay:
                return False
        
        self._cooldowns[key] = now
        return True
    
    def reset(self, user_id: int, command: str) -> None:
        """
        Reset cooldown for a user command.
        
        Args:
            user_id: User ID
            command: Command name
        """
        key = f"{user_id}:{command}"
        if key in self._cooldowns:
            del self._cooldowns[key]
    
    def clear(self) -> None:
        """Clear all cooldowns."""
        self._cooldowns.clear()
    
    def get_remaining(self, user_id: int, command: str, delay: Optional[int] = None) -> int:
        """
        Get remaining cooldown time for a user command.
        
        Args:
            user_id: User ID
            command: Command name
            delay: Optional custom delay
            
        Returns:
            Remaining time in seconds (0 if no cooldown)
        """
        delay = delay or self.default_delay
        key = f"{user_id}:{command}"
        
        if key in self._cooldowns:
            elapsed = time.time() - self._cooldowns[key]
            if elapsed < delay:
                return int(delay - elapsed)
        
        return 0
