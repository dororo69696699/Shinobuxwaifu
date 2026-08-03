from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from config import MONGO_URI, DB_NAME

_db: AsyncIOMotorDatabase = None


async def init_db() -> None:
    """Initialize MongoDB connection and setup indexes."""
    global _db
    client = AsyncIOMotorClient(MONGO_URI)
    _db = client[DB_NAME]
    
    await _db.users.create_index("id", unique=True)
    await _db.users.create_index("username")
    await _db.characters.create_index("id", unique=True)
    await _db.characters.create_index("name")


def get_db() -> AsyncIOMotorDatabase:
    """Get the active database instance."""
    if _db is None:
        raise RuntimeError("Database not initialized! Ensure init_db() is called on startup.")
    return _db


def get_collection(name: str):
    """Retrieve a MongoDB collection by name safely."""
    return get_db()[name]
