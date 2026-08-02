# ==========================================
# Admin Commands Help
# ==========================================

"""
Help entries for admin commands.
"""

from app.assets.help import HelpEntry


ADMIN_HELP = {
    "addchar": HelpEntry(
        name="addchar",
        display_name="📝 Add Character",
        description="Request to add a new character to the database.",
        usage="/addchar name anime rarity (reply to image)",
        examples=[
            "/addchar Naruto Naruto 1 - Add common Naruto",
            "Rarity numbers: 0=Common, 1=Medium, 2=Rare, 3=Legendary, 4=Celestial",
        ],
        notes=[
            "Reply to an image with the command",
            "Admins can approve or reject requests",
            "Rarity options: Common, Rare, Legendary, Medium, Celestial, etc.",
        ],
    ),
    
    "upload": HelpEntry(
        name="upload",
        display_name="📤 Upload Character (Admin)",
        description="Directly upload a character to the database.",
        usage="/upload name anime rarity (reply to image)",
        examples=[
            "/upload Naruto Naruto 1 - Upload Naruto",
            "/gupload - Alternative command",
        ],
        notes=[
            "Admin only command",
            "No approval needed",
            "Use /server to change upload server (ImgBB/Catbox)",
        ],
    ),
    
    "broadcast": HelpEntry(
        name="broadcast",
        display_name="📢 Broadcast (Admin)",
        description="Send a message to all users.",
        usage="/broadcast <message>",
        examples=[
            "/broadcast Hello everyone!",
        ],
        notes=[
            "Admin only command",
            "Only owner and broadcast admins can use",
            "Rate limited to prevent spam",
        ],
    ),
    
    "stats": HelpEntry(
        name="stats",
        display_name="📊 Bot Stats (Admin)",
        description="View bot statistics and database info.",
        usage="/stats",
        examples=[
            "/stats - View bot statistics",
        ],
        notes=[
            "Admin only command",
            "Shows user count, character count, and more",
        ],
    ),
    
    "redeem": HelpEntry(
        name="redeem",
        display_name="🎫 Redeem Codes (Admin)",
        description="Create and manage redeem codes.",
        usage="/createredeem <amount> <uses>",
        examples=[
            "/createredeem 1000 10 - Create code for 1000 coins, 10 uses",
        ],
        notes=[
            "Admin only command",
            "Users redeem with /redeem <code>",
        ],
    ),
}
