from datetime import datetime
from typing import Optional

from database.manager import get_collection

users_collection = get_collection("users")
characters_collection = get_collection("characters")
sudo_collection = get_collection("sudo_users")


async def register_user(user_id: int, username: str, first_name: str, last_name: str = None) -> None:
    existing = await users_collection.find_one({"id": user_id})
    if not existing:
        await users_collection.insert_one({
            "id": user_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "balance": 0,
            "tokens": 0,
            "characters": [],
            "last_daily": None,
            "last_weekly": None,
            "created_at": datetime.now(),
        })


async def get_user(user_id: int) -> Optional[dict]:
    return await users_collection.find_one({"id": user_id})


async def get_user_by_username(username: str) -> Optional[dict]:
    return await users_collection.find_one({"username": username})


async def get_user_balance(user_id: int) -> int:
    user = await get_user(user_id)
    return user.get("balance", 0) if user else 0


async def add_balance(user_id: int, amount: int) -> None:
    await users_collection.update_one(
        {"id": user_id},
        {"$inc": {"balance": amount}},
        upsert=True,
    )


async def update_user(user_id: int, data: dict) -> None:
    await users_collection.update_one(
        {"id": user_id},
        {"$set": data},
        upsert=True,
    )


async def delete_user(user_id: int) -> None:
    await users_collection.delete_one({"id": user_id})


async def is_vip(user_id: int) -> bool:
    sudo = await sudo_collection.find_one({"_id": user_id})
    return sudo and "VIP" in sudo.get("powers", [])
