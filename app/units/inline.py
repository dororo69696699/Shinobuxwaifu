# ==========================================
# 
# Rewritten with Clean Architecture
# ==========================================

"""
Inline Search and Caching Service

Provides caching and search functionality for inline queries including:
- Character search by name, anime, aliases
- User collection lookup with caching
- Cache invalidation and refresh
- Pagination support for search results
"""

import asyncio
import logging
import re
from typing import List, Optional, Dict, Any, Union
from datetime import datetime, timedelta
from functools import wraps

from app.database.repositories.character import CharacterRepository
from app.database.repositories.user import UserRepository
from app.database.models.character import Character
from app.database.models.user import User

logger = logging.getLogger(__name__)


class CacheEntry:
    """
    A cache entry with expiration tracking.
    """
    
    def __init__(self, value: Any, ttl_seconds: int):
        """
        Initialize a cache entry.
        
        Args:
            value: The cached value
            ttl_seconds: Time to live in seconds
        """
        self.value = value
        self.expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)
    
    def is_expired(self) -> bool:
        """
        Check if the cache entry has expired.
        
        Returns:
            True if expired, False otherwise
        """
        return datetime.utcnow() > self.expires_at


class AsyncCache:
    """
    Async-safe cache with TTL support.
    """
    
    def __init__(self, default_ttl: int = 300):
        """
        Initialize the cache.
        
        Args:
            default_ttl: Default TTL in seconds
        """
        self._cache: Dict[str, CacheEntry] = {}
        self._default_ttl = default_ttl
        self._lock = asyncio.Lock()
    
    async def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value if found and not expired, None otherwise
        """
        async with self._lock:
            entry = self._cache.get(key)
            if entry and not entry.is_expired():
                return entry.value
            if entry:
                # Remove expired entry
                del self._cache[key]
            return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Set a value in the cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Optional TTL override
        """
        ttl = ttl or self._default_ttl
        async with self._lock:
            self._cache[key] = CacheEntry(value, ttl)
    
    async def delete(self, key: str) -> None:
        """
        Delete a value from the cache.
        
        Args:
            key: Cache key
        """
        async with self._lock:
            if key in self._cache:
                del self._cache[key]
    
    async def clear(self) -> None:
        """
        Clear all cache entries.
        """
        async with self._lock:
            self._cache.clear()
    
    async def cleanup(self) -> None:
        """
        Remove all expired entries.
        """
        async with self._lock:
            expired_keys = [
                key for key, entry in self._cache.items()
                if entry.is_expired()
            ]
            for key in expired_keys:
                del self._cache[key]


class InlineSearchService:
    """
    Service for inline search and caching operations.
    """
    
    def __init__(
        self,
        character_repo: CharacterRepository,
        user_repo: UserRepository,
        character_cache_ttl: int = 300,
        user_cache_ttl: int = 30,
        search_cache_ttl: int = 60,
    ):
        """
        Initialize the inline search service.
        
        Args:
            character_repo: Character repository
            user_repo: User repository
            character_cache_ttl: Character cache TTL in seconds
            user_cache_ttl: User cache TTL in seconds
            search_cache_ttl: Search results cache TTL in seconds
        """
        self.character_repo = character_repo
        self.user_repo = user_repo
        
        # Initialize caches
        self.character_cache = AsyncCache(default_ttl=character_cache_ttl)
        self.user_cache = AsyncCache(default_ttl=user_cache_ttl)
        self.search_cache = AsyncCache(default_ttl=search_cache_ttl)
        
        # Cache keys
        self.ALL_CHARACTERS_KEY = "all_characters"
        self.USER_PREFIX = "user_"
        self.SEARCH_PREFIX = "search_"
    
    # ===== User Collection Methods =====
    
    async def get_user_collection(
        self,
        user_id: int,
        force_refresh: bool = False
    ) -> Optional[User]:
        """
        Get a user's character collection from database with caching.
        
        Args:
            user_id: Telegram user ID
            force_refresh: Force refresh from database
            
        Returns:
            User object if found, None otherwise
        """
        cache_key = f"{self.USER_PREFIX}{user_id}"
        
        # Check cache
        if not force_refresh:
            cached = await self.user_cache.get(cache_key)
            if cached is not None:
                logger.debug(f"User {user_id} found in cache")
                return cached
        
        # Fetch from database
        try:
            user = await self.user_repo.get_by_id(user_id)
            if user:
                await self.user_cache.set(cache_key, user)
                logger.debug(f"User {user_id} cached from database")
            return user
        except Exception as e:
            logger.error(f"Failed to fetch user {user_id}: {e}")
            return None
    
    async def get_user_characters(
        self,
        user_id: int,
        force_refresh: bool = False
    ) -> List[Character]:
        """
        Get all characters owned by a user.
        
        Args:
            user_id: Telegram user ID
            force_refresh: Force refresh from database
            
        Returns:
            List of Character objects
        """
        user = await self.get_user_collection(user_id, force_refresh)
        if not user:
            return []
        
        # Get character details for each ID in user's collection
        characters = []
        for char_id in user.characters:
            char = await self.character_repo.get_by_id(char_id)
            if char:
                characters.append(char)
        
        return characters
    
    # ===== Character Search Methods =====
    
    async def search_characters(
        self,
        query: str,
        limit: int = 50,
        offset: int = 0,
        force_refresh: bool = False
    ) -> List[Character]:
        """
        Search characters by name, anime, or aliases.
        
        Args:
            query: Search query
            limit: Maximum results to return
            offset: Results offset for pagination
            force_refresh: Force refresh from database
            
        Returns:
            List of matching Character objects
        """
        if not query or len(query.strip()) < 1:
            return []
        
        # Normalize query
        query = query.strip()
        cache_key = f"{self.SEARCH_PREFIX}{query.lower()}"
        
        # Check cache
        if not force_refresh:
            cached = await self.search_cache.get(cache_key)
            if cached is not None:
                logger.debug(f"Search '{query}' found in cache")
                # Apply pagination to cached results
                return cached[offset:offset + limit]
        
        # Perform search
        try:
            # Build regex pattern
            pattern = re.compile(query, re.IGNORECASE)
            
            # Search in multiple fields
            characters = await self.character_repo.search(
                fields=["name", "anime", "aliases"],
                pattern=pattern,
                limit=limit + offset,  # Fetch extra for pagination
            )
            
            # Cache full results
            await self.search_cache.set(cache_key, characters)
            logger.debug(f"Search '{query}' cached with {len(characters)} results")
            
            # Apply pagination
            return characters[offset:offset + limit]
            
        except Exception as e:
            logger.error(f"Failed to search characters for '{query}': {e}")
            return []
    
    async def get_all_characters(
        self,
        force_refresh: bool = False
    ) -> List[Character]:
        """
        Get all characters from database with caching.
        
        Args:
            force_refresh: Force refresh from database
            
        Returns:
            List of all Character objects
        """
        # Check cache
        if not force_refresh:
            cached = await self.character_cache.get(self.ALL_CHARACTERS_KEY)
            if cached is not None:
                logger.debug("All characters found in cache")
                return cached
        
        # Fetch from database
        try:
            characters = await self.character_repo.get_all()
            await self.character_cache.set(self.ALL_CHARACTERS_KEY, characters)
            logger.debug(f"All characters cached: {len(characters)} characters")
            return characters
        except Exception as e:
            logger.error(f"Failed to fetch all characters: {e}")
            return []
    
    async def get_character_by_id(self, character_id: int) -> Optional[Character]:
        """
        Get a single character by ID.
        
        Args:
            character_id: Character ID
            
        Returns:
            Character object if found, None otherwise
        """
        # Try all characters cache first
        all_chars = await self.get_all_characters()
        for char in all_chars:
            if char.id == character_id:
                return char
        
        # Fallback to database
        try:
            return await self.character_repo.get_by_id(character_id)
        except Exception as e:
            logger.error(f"Failed to fetch character {character_id}: {e}")
            return None
    
    # ===== Cache Management Methods =====
    
    async def refresh_caches(self) -> None:
        """
        Force refresh all caches.
        """
        await self.character_cache.clear()
        await self.user_cache.clear()
        await self.search_cache.clear()
        logger.info("All caches cleared")
    
    async def refresh_user_cache(self, user_id: int) -> None:
        """
        Refresh cache for a specific user.
        
        Args:
            user_id: User ID to refresh
        """
        cache_key = f"{self.USER_PREFIX}{user_id}"
        await self.user_cache.delete(cache_key)
        logger.debug(f"User cache cleared for {user_id}")
    
    async def refresh_search_cache(self, query: str) -> None:
        """
        Refresh cache for a specific search query.
        
        Args:
            query: Search query to refresh
        """
        cache_key = f"{self.SEARCH_PREFIX}{query.lower()}"
        await self.search_cache.delete(cache_key)
        logger.debug(f"Search cache cleared for '{query}'")
    
    async def cleanup_caches(self) -> None:
        """
        Clean up expired cache entries.
        """
        await self.character_cache.cleanup()
        await self.user_cache.cleanup()
        await self.search_cache.cleanup()
    
    # ===== Utility Methods =====
    
    def extract_user_id_from_query(self, query: str) -> Optional[int]:
        """
        Extract user ID from inline query for collection lookups.
        
        Args:
            query: Inline query string
            
        Returns:
            User ID if found, None otherwise
        """
        # Check for collection pattern: collection.12345
        match = re.match(r'collection\.(\d+)', query)
        if match:
            return int(match.group(1))
        return None
    
    def is_amv_query(self, query: str) -> bool:
        """
        Check if query is for AMV/video-only results.
        
        Args:
            query: Inline query string
            
        Returns:
            True if AMV filter is requested
        """
        return query.lower().endswith('.amv')


# ===== Factory Function =====

def create_inline_search_service(config) -> InlineSearchService:
    """
    Create an inline search service instance.
    
    Args:
        config: Bot configuration
        
    Returns:
        InlineSearchService instance
    """
    from app.database.manager import get_db_manager
    from app.database.repositories.character import CharacterRepository
    from app.database.repositories.user import UserRepository
    
    db_manager = get_db_manager()
    character_repo = CharacterRepository(db_manager)
    user_repo = UserRepository(db_manager)
    
    return InlineSearchService(
        character_repo=character_repo,
        user_repo=user_repo,
        character_cache_ttl=config.INLINE_CACHE_TTL or 300,
        user_cache_ttl=config.USER_CACHE_TTL or 30,
        search_cache_ttl=config.SEARCH_CACHE_TTL or 60,
    )


# ===== Backward Compatibility =====

class LegacyInlineCompat:
    """
    Backward compatibility wrapper for old inline functions.
    """
    
    def __init__(self):
        self._service: Optional[InlineSearchService] = None
    
    @property
    def service(self) -> InlineSearchService:
        if self._service is None:
            from app.core.config import get_config
            config = get_config()
            self._service = create_inline_search_service(config)
        return self._service
    
    async def get_user_collection(self, user_id: int) -> Optional[Dict]:
        """
        Legacy get_user_collection function.
        """
        user = await self.service.get_user_collection(user_id)
        if user:
            return user.to_dict()
        return None
    
    async def search_characters(
        self,
        query: str,
        force_refresh: bool = False
    ) -> List[Dict]:
        """
        Legacy search_characters function.
        """
        characters = await self.service.search_characters(
            query,
            force_refresh=force_refresh
        )
        return [char.to_dict() for char in characters]
    
    async def get_all_characters(self, force_refresh: bool = False) -> List[Dict]:
        """
        Legacy get_all_characters function.
        """
        characters = await self.service.get_all_characters(force_refresh)
        return [char.to_dict() for char in characters]
    
    async def refresh_character_caches(self) -> None:
        """
        Legacy refresh_character_caches function.
        """
        await self.service.refresh_caches()


# Create singleton for backward compatibility
legacy_inline = LegacyInlineCompat()

# For old code that imported these functions directly
get_user_collection = legacy_inline.get_user_collection
search_characters = legacy_inline.search_characters
get_all_characters = legacy_inline.get_all_characters
refresh_character_caches = legacy_inline.refresh_character_caches
