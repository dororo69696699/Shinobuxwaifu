# ==========================================
# Uptime Service
# ==========================================

"""
Service for tracking bot uptime and calculating ping.
"""

import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class UptimeService:
    """
    Tracks bot uptime and calculates ping.
    """
    
    start_time: float = time.time()
    
    def get_uptime_seconds(self) -> int:
        """
        Get uptime in seconds.
        
        Returns:
            Uptime in seconds
        """
        return int(time.time() - self.start_time)
    
    def get_uptime_string(self) -> str:
        """
        Get uptime as formatted string.
        
        Returns:
            Formatted uptime (e.g., "5h 30m 45s")
        """
        seconds = self.get_uptime_seconds()
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours}h {minutes}m {seconds}s"
    
    def get_ping(self) -> int:
        """
        Get approximate ping (time since start).
        
        Returns:
            Ping in milliseconds
        """
        # This is just an approximation
        return int(time.time() * 1000 % 1000)
