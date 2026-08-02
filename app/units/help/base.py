# ==========================================
# Base Help Templates
# ==========================================

"""
Base templates and constants for help system.
"""

from app.assets.help import HelpEntry

# Constants that can be referenced in help entries
CONSTANTS = {
    "DAILY_REWARD": "40",
    "MIN_BET": "100",
    "MAX_BET": "50,000",
    "JACKPOT_WIN": "2000",
    "GIFT_TIMEOUT": "1 hour",
}

# Common notes
COMMON_NOTES = [
    "All amounts are in coins",
    "Bot must be admin in groups for some features to work",
]

# Base template for game commands
def create_game_entry(
    name: str,
    display_name: str,
    description: str,
    usage: str,
    examples: List[str],
    rules: List[str],
    limits: List[str],
) -> HelpEntry:
    """Create a standardized game help entry."""
    notes = []
    notes.extend(rules)
    notes.extend(limits)
    return HelpEntry(
        name=name,
        display_name=display_name,
        description=description,
        usage=usage,
        examples=examples,
        notes=notes,
)
