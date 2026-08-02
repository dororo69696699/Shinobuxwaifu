# Add to UserRepository class:

async def get_balance(self, user_id: int) -> int:
    """
    Get a user's balance.
    
    Args:
        user_id: User ID
        
    Returns:
        Balance amount
    """
    user = await self.get_by_id(user_id)
    return user.balance if user else 0

async def add_balance(self, user_id: int, amount: int) -> None:
    """
    Add or subtract from a user's balance.
    
    Args:
        user_id: User ID
        amount: Amount to add (negative to subtract)
    """
    await self.collection.update_one(
        {"_id": user_id},
        {"$inc": {"balance": amount}},
        upsert=True,
    )

async def set_balance(self, user_id: int, amount: int) -> None:
    """
    Set a user's balance.
    
    Args:
        user_id: User ID
        amount: New balance amount
    """
    await self.collection.update_one(
        {"_id": user_id},
        {"$set": {"balance": amount}},
        upsert=True,
    )

async def update_last_daily(self, user_id: int) -> None:
    """
    Update the last daily claim time.
    
    Args:
        user_id: User ID
    """
    await self.collection.update_one(
        {"_id": user_id},
        {"$set": {"last_daily": datetime.utcnow()}},
        upsert=True,
    )

async def update_last_weekly(self, user_id: int) -> None:
    """
    Update the last weekly claim time.
    
    Args:
        user_id: User ID
    """
    await self.collection.update_one(
        {"_id": user_id},
        {"$set": {"last_weekly": datetime.utcnow()}},
        upsert=True,
    )

async def get_by_username(self, username: str) -> Optional[User]:
    """
    Get a user by username.
    
    Args:
        username: Telegram username (without @)
        
    Returns:
        User if found, None otherwise
    """
    data = await self.collection.find_one({"username": username})
    if data:
        return User.from_dict(data)
    return None

async def update_characters(self, user_id: int, character_ids: List[int]) -> None:
    """
    Update a user's character list.
    
    Args:
        user_id: User ID
        character_ids: List of character IDs
    """
    await self.collection.update_one(
        {"_id": user_id},
        {"$set": {"characters": character_ids}},
        upsert=True,
    )

async def delete(self, user_id: int) -> bool:
    """
    Delete a user from the database.
    
    Args:
        user_id: User ID
        
    Returns:
        True if deleted, False otherwise
    """
    result = await self.collection.delete_one({"_id": user_id})
    return result.deleted_count > 0
