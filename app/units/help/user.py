# ==========================================
# User Commands Help
# ==========================================

"""
Help entries for standard user commands.
"""

from app.assets.help import HelpEntry


USER_HELP = {
    "balance": HelpEntry(
        name="balance",
        display_name="💰 Balance & Pay",
        description="Check your balance or send coins to other users.",
        usage="/balance [@username|user_id]",
        examples=[
            "/balance - Check your balance",
            "/balance @username - Check another user's balance",
            "/pay 100 @username - Send 100 coins to a user",
        ],
        notes=[
            "You must have enough balance to send coins",
            "Payments are final and cannot be reversed",
        ],
    ),
    
    "profile": HelpEntry(
        name="profile",
        display_name="👤 Profile",
        description="View your profile or another user's profile.",
        usage="/profile [@username|user_id]",
        examples=[
            "/profile - View your profile",
            "/profile @username - View another user's profile",
        ],
        notes=[],
    ),
    
    "check": HelpEntry(
        name="check",
        display_name="🔍 Check Character",
        description="View details of a specific character by ID.",
        usage="/check <character_id>",
        examples=[
            "/check 12345 - View character with ID 12345",
        ],
        notes=[
            "Displays character name, anime, rarity, and image",
            "Shows top 10 owners of the character",
        ],
    ),
    
    "harem": HelpEntry(
        name="harem",
        display_name="🌸 Harem Collection",
        description="View your collected characters.",
        usage="/harem or /collection",
        examples=[
            "/harem - View your collection",
            "/collection - Alternative command",
        ],
        notes=[
            "Navigate pages using the buttons",
            "Filter by rarity using the filter button",
            "Characters are grouped by anime",
        ],
    ),
    
    "favorites": HelpEntry(
        name="favorites",
        display_name="⭐ Favorites",
        description="Add characters to your favorites list.",
        usage="/fav <character_id>",
        examples=[
            "/fav 12345 - Add character 12345 to favorites",
        ],
        notes=[
            "Only characters in your collection can be favorited",
            "Confirm with '✅ Yes' or cancel with '❎ No'",
        ],
    ),
}
