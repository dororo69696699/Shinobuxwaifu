# ==========================================
# Games Help
# ==========================================

"""
Help entries for game commands.
"""

from app.assets.help import HelpEntry


GAMES_HELP = {
    "guess": HelpEntry(
        name="guess",
        display_name="🎯 Guess the Character",
        description="Guess the mystery character to earn coins and capture them.",
        usage="/guess <character_name>",
        examples=[
            "/guess Naruto - Guess the character",
        ],
        notes=[
            "Earn 40 coins for a correct guess",
            "The first correct guess captures the character",
            "If incorrect, you can try again",
        ],
    ),
    
    "gacha": HelpEntry(
        name="gacha",
        display_name="🎰 Gacha Roll",
        description="Roll for random characters with varying rarities.",
        usage="/gacha [amount]",
        examples=[
            "/gacha - Roll once (100 coins)",
            "/gacha 5 - Roll 5 times (500 coins)",
        ],
        notes=[
            "Base cost: 100 coins per roll",
            "Higher rarities have lower drop rates",
            "Characters are added to your collection",
        ],
    ),
    
    "coinflip": HelpEntry(
        name="coinflip",
        display_name="🪙 Coinflip",
        description="Bet on heads or tails for a 2x payout.",
        usage="/coinflip <amount> <heads/tails>",
        examples=[
            "/coinflip 100 heads - Bet 100 coins on heads",
            "/toss 500 tails - Alternative command",
        ],
        notes=[
            f"Minimum bet: {CONSTANTS['MIN_BET']} coins",
            f"Maximum bet: {CONSTANTS['MAX_BET']} coins",
            "Correct guess pays 2x your bet",
        ],
    ),
    
    "slots": HelpEntry(
        name="slots",
        display_name="🎰 Slots",
        description="Spin the slot machine with 3 reels.",
        usage="/slot <amount>",
        examples=[
            "/slot 1000 - Spin with 1000 coins",
            "/slots 500 - Alternative command",
        ],
        notes=[
            f"Minimum bet: {CONSTANTS['MIN_BET']} coins",
            f"Maximum bet: {CONSTANTS['MAX_BET']} coins",
            "3 matching emojis: 5x payout",
            "2 matching emojis: 1.5x payout",
            "0 matching: Bet is lost",
        ],
    ),
    
    "blackjack": HelpEntry(
        name="blackjack",
        display_name="🃏 Blackjack",
        description="Play blackjack against the dealer.",
        usage="/bj <amount>",
        examples=[
            "/bj 1000 - Start a blackjack game",
            "/blackjack 500 - Alternative command",
        ],
        notes=[
            f"Minimum bet: {CONSTANTS['MIN_BET']} coins",
            f"Maximum bet: {CONSTANTS['MAX_BET']} coins",
            "Standard win: 2.0x payout",
            "Natural Blackjack: 2.5x payout",
            "Push (Tie): Bet refunded",
            "Use 'Hit' to draw, 'Stand' to end turn",
        ],
    ),
    
    "mines": HelpEntry(
        name="mines",
        display_name="💣 Minesweeper",
        description="Sweep mines on a 4x4 grid for big rewards.",
        usage="/mines [bet] [mines]",
        examples=[
            "/mines - Start with default 1000 coins, 3 mines",
            "/mines 5000 5 - Bet 5000 with 5 mines",
        ],
        notes=[
            "Minimum bet: 500 coins",
            "Maximum bet: 100,000 coins",
            "Mines: 3-5 (default: 3)",
            "Hitting 4+ safe cells gives a chance at bonus characters",
            "Cashout anytime with Claim button",
        ],
    ),
    
    "wheel": HelpEntry(
        name="wheel",
        display_name="🎡 Wheel of Fortune",
        description="Spin the wheel for random rewards.",
        usage="/spin <amount>",
        examples=[
            "/spin 1000 - Spin with 1000 coins",
            "/wheel 500 - Alternative command",
        ],
        notes=[
            f"Minimum bet: {CONSTANTS['MIN_BET']} coins",
            f"Maximum bet: {CONSTANTS['MAX_BET']} coins",
            "Sectors: Bust (0x), Half (0.5x), Push (1x)",
            "Win (1.5x), Double (2x), Jackpot (5x)",
            "1% chance for Waifu Drop (Legendary/Celestial)",
        ],
    ),
    
    "highlow": HelpEntry(
        name="highlow",
        display_name="🃏 High Low",
        description="Guess if the next card is higher or lower.",
        usage="/hl <amount>",
        examples=[
            "/hl 1000 - Start a High Low game",
            "/highlow 500 - Alternative command",
        ],
        notes=[
            f"Minimum bet: {CONSTANTS['MIN_BET']} coins",
            f"Maximum bet: {CONSTANTS['MAX_BET']} coins",
            "Streak 1: 1.4x, Streak 2: 1.8x",
            "Streak 3: 2.2x, Streak 4: 2.6x",
            "Use 'Cashout' to claim winnings anytime",
        ],
    ),
    
    "ox": HelpEntry(
        name="ox",
        display_name="⭕ Tic Tac Toe",
        description="Challenge players to Tic Tac Toe with betting.",
        usage="/ox <bet>",
        examples=[
            "/ox 1000 - Host a game with 1000 coin bet",
            "/oxstats - View your stats",
            "/oxtop - View leaderboard",
        ],
        notes=[
            "Bet range: 100-100,000 coins",
            "Two players with matching bets",
            "2-minute turn timer",
            "Draw: Both refunded",
            "Win: Takes the entire prize pool (2x bet)",
        ],
    ),
    
    "demonslayer": HelpEntry(
        name="demonslayer",
        display_name="⚔️ Demon Slayer RPG",
        description="Embark on a demon-slaying adventure!",
        usage="/demonslayer",
        examples=[
            "/demonslayer - View your RPG profile",
            "/hunt - Hunt demons for XP and trophies",
            "/dprofile - View detailed profile",
            "/challenge - Challenge another player to PvP",
            "/dtop - View monthly leaderboard",
        ],
        notes=[
            "Choose a Hashira mentor for unique abilities",
            "Battle demons with interactive combat",
            "Level up and progress through 11 ranks",
            "PvP battles with other slayers",
            "Reward milestones at 100/250/500/1000 trophies",
        ],
    ),
}
