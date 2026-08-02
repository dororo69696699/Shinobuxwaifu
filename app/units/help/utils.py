# ==========================================
# Utility Commands Help
# ==========================================

"""
Help entries for utility commands.
"""

from app.assets.help import HelpEntry


UTILS_HELP = {
    "inline": HelpEntry(
        name="inline",
        display_name="🔎 Inline Search",
        description="Search for characters using inline queries.",
        usage="@{BOT_USERNAME} <query>",
        examples=[
            "@{BOT_USERNAME} Naruto - Search for Naruto",
            "@{BOT_USERNAME} collection.12345 - View user collection",
            "@{BOT_USERNAME} collection.12345 Naruto - Search in collection",
            "@{BOT_USERNAME} Naruto.AMV - Show video clips",
        ],
        notes=[
            "Results show character name, anime, rarity, and image",
            "Use .AMV to filter video-only results",
        ],
    ),
    
    "rankings": HelpEntry(
        name="rankings",
        display_name="🏆 Rankings",
        description="View global leaderboards.",
        usage="/rank",
        examples=[
            "/rank - View top 10 users",
        ],
        notes=[
            "Categories: Top Users (most characters)",
            "Top Groups (most guesses)",
            "MTOP (highest coin balance)",
            "Use buttons to switch categories",
        ],
    ),
    
    "sips": HelpEntry(
        name="sips",
        display_name="🔍 Search Characters",
        description="Search for characters by name.",
        usage="/sips <character_name>",
        examples=[
            "/sips Naruto - Search for Naruto",
        ],
        notes=[
            "Pagination buttons if multiple results found",
            "Shows character name, anime, ID, and rarity",
        ],
    ),
    
    "transfer": HelpEntry(
        name="transfer",
        display_name="📦 Transfer Collection (VIP)",
        description="Transfer all characters to another user.",
        usage="/transfer <user_id> <owner_id>",
        examples=[
            "/transfer 12345 67890 - Transfer from 12345 to 67890",
            "/backtransfer <transfer_id> - Revert a transfer (1 hour)",
        ],
        notes=[
            "VIP only command",
            "All characters are transferred",
            "Undo within 1 hour with /backtransfer",
        ],
    ),
    
    "bounty": HelpEntry(
        name="bounty",
        display_name="🏴‍☠️ Wanted Poster",
        description="Generate a One Piece-style wanted poster.",
        usage="/bounty [@username]",
        examples=[
            "/bounty - Your own poster",
            "/bounty @username - Someone else's poster",
        ],
        notes=[
            "Uses your profile picture",
            "Shows your balance as bounty",
            "Custom Berry symbol (฿) included",
        ],
    ),
}
