from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from config import MONGO_URI, DB_NAME

_db: AsyncIOMotorDatabase = None


async def init_db() -> None:
    global _db
    client = AsyncIOMotorClient(MONGO_URI)
    _db = client[DB_NAME]
    
    await _db.users.create_index("id", unique=True)
    await _db.users.create_index("username")
    await _db.characters.create_index("id", unique=True)
    await _db.characters.create_index("name")


def get_db() -> AsyncIOMotorDatabase:
    return _db


def get_collection(name: str):
    return _db[name]
