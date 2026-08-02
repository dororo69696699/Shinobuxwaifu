# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
Inline Search and Cache Utilities
"""

import re
from cachetools import TTLCache
from database.models import get_collection

# Caches
all_characters_cache = TTLCache(maxsize=10000, ttl=300)
user_collection_cache = TTLCache(maxsize=10000, ttl=30)


async def get_user_collection(user_id):
    """Get user collection from database with caching."""
    user_id = str(user_id)
    if user_id in user_collection_cache:
        return user_collection_cache[user_id]
    
    users_collection = get_collection("users")
    user = await users_collection.find_one({'id': int(user_id)})
    if user:
        user_collection_cache[user_id] = user
    return user


async def search_characters(query, force_refresh=False):
    """Search characters by name, anime, or aliases."""
    cache_key = f"search_{query.lower()}"
    if not force_refresh and cache_key in all_characters_cache:
        return all_characters_cache[cache_key]
    
    collection = get_collection("characters")
    regex = re.compile(query, re.IGNORECASE)
    characters = await collection.find({
        "$or": [
            {"name": regex},
            {"anime": regex},
            {"aliases": regex}
        ]
    }).to_list(length=None)
    
    all_characters_cache[cache_key] = characters
    return characters


async def get_all_characters(force_refresh=False):
    """Get all characters with caching."""
    if not force_refresh and 'all_characters' in all_characters_cache:
        return all_characters_cache['all_characters']
    
    collection = get_collection("characters")
    characters = await collection.find({}).to_list(length=None)
    all_characters_cache['all_characters'] = characters
    return characters


async def refresh_character_caches():
    """Force refresh all caches."""
    all_characters_cache.clear()
    user_collection_cache.clear()
