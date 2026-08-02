# ==========================================
# Economy Commands Help
# ==========================================

"""
Help entries for economy and shop commands.
"""

from app.assets.help import HelpEntry


ECONOMY_HELP = {
    "shop": HelpEntry(
        name="shop",
        display_name="🛒 Shop",
        description="Browse and purchase characters from the shop.",
        usage="/shop",
        examples=[
            "/shop - Open the shop menu",
            "/hshopmenu - Alternative command",
        ],
        notes=[
            "Make sure you have enough balance!",
            "Use the 'Next' button to view more characters",
            "Admin can add items with /addshop",
        ],
    ),
    
    "gift": HelpEntry(
        name="gift",
        display_name="🎁 Gift System",
        description="Send characters to other users.",
        usage="/gift <character_id> (reply to user)",
        examples=[
            "Reply to a user's message and use /gift 12345",
        ],
        notes=[
            "Receiver must confirm the gift",
            "Auto-canceled if not confirmed within 1 hour",
            "Only characters in your collection can be gifted",
        ],
    ),
    
    "claim": HelpEntry(
        name="claim",
        display_name="🎁 Daily Claim",
        description="Claim a free character every day!",
        usage="/hclaim or /claim",
        examples=[
            "/claim - Claim your daily character",
            "/hclaim - Alternative command",
        ],
        notes=[
            "You must be in the required channel to claim",
            "One claim per day",
            "Characters are unique and not repeated",
        ],
    ),
    
    "daily": HelpEntry(
        name="daily",
        display_name="📅 Daily Rewards",
        description="Claim your daily coin rewards.",
        usage="/daily",
        examples=[
            "/daily - Claim daily coins",
        ],
        notes=[
            "One claim per day",
            "Reward amount depends on your streak",
        ],
    ),
}
