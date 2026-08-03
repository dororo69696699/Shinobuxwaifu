import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_env_int(key: str, default: int = 0) -> int:
    """Safely parse integer environment variables."""
    try:
        return int(os.getenv(key, str(default)))
    except ValueError:
        return default


def get_env_list(key: str, default: list = None) -> list:
    """Parse comma-separated strings into a clean list."""
    if default is None:
        default = []
    val = os.getenv(key)
    if not val:
        return default
    return [item.strip() for item in val.split(",") if item.strip()]


# Core Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
MONGO_URI = os.getenv("MONGO_URI", "")
DB_NAME = os.getenv("DB_NAME", "WAIFUBOT")

# Security & Ownership
OWNER_ID = get_env_int("OWNER_ID", 0)
SUDO_USERS = [get_env_int(x) for x in get_env_list("SUDO_USERS") if x.isdigit()]
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "EGOIST_6969")

# Channels & Logs
FORCE_JOIN = os.getenv("FORCE_JOIN", "")
BOT_LOGGING = os.getenv("BOT_LOGGING", "")
SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", "https://t.me/+fPjchISAGnc3OGJl")
UPDATE_CHAT = os.getenv("UPDATE_CHAT", "https://t.me/+wjJbHQ9DQzM1OTE1")
FORCE_JOIN_LINK = os.getenv("FORCE_JOIN_LINK", UPDATE_CHAT)

# Economy & Rewards
DAILY_REWARD = get_env_int("DAILY_REWARD", 100)
WEEKLY_REWARD = get_env_int("WEEKLY_REWARD", 2000)

# Media Assets
START_MEDIA = [
    os.getenv("START_MEDIA_1", "https://files.catbox.moe/5zrb1a.mp4"),
    os.getenv("START_MEDIA_2", "https://files.catbox.moe/5zrb1a.mp4"),
]
