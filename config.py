
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
MONGO_URI = os.getenv("MONGO_URI", "")
DB_NAME = os.getenv("DB_NAME", "WAIFUBOT")
FORCE_JOIN = os.getenv("FORCE_JOIN", "")
BOT_LOGGING = os.getenv("BOT_LOGGING", "")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
DAILY_REWARD = int(os.getenv("DAILY_REWARD", "100"))
WEEKLY_REWARD = int(os.getenv("WEEKLY_REWARD", "2000"))

START_MEDIA = [
    os.getenv("START_MEDIA_1", "https://files.catbox.moe/5zrb1a.mp4"),
    os.getenv("START_MEDIA_2", "https://files.catbox.moe/5zrb1a.mp4")
]

SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", "https://t.me/+fPjchISAGnc3OGJl")
UPDATE_CHAT = os.getenv("UPDATE_CHAT", "https://t.me/+wjJbHQ9DQzM1OTE1")
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "EGOIST_6969")
