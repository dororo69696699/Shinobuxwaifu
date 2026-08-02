# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
Minesweeper - Casino style betting game
"""

import math
import random
import uuid
from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.enums import ParseMode

from database.models import get_user, update_user, add_balance, get_user_balance, get_collection

router = Router(name="mines")

GRID_SIZE = 4
MIN_BET = 500
MAX_BET = 100000
MIN_MINES = 3
MAX_MINES = 5


def nCr(n, r):
    if r < 0 or r > n:
        return 0
    return math.comb(n, r)


def get_multiplier(num_mines, safe_opened):
    """Calculate multiplier based on probability."""
    if safe_opened <= 0:
        return 1.0
    total_cells = GRID_SIZE * GRID_SIZE
    total_ways = nCr(total_cells, safe_opened)
    safe_ways = nCr(total_cells - num_mines, safe_opened)
    if safe_ways == 0:
        return 0.0
    mult = total_ways / safe_ways
    return round(mult * 0.95, 2)


def create_game(num_mines):
    """Create game grid and place mines."""
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    total_cells = GRID_SIZE * GRID_SIZE
    mines_indices = random.sample(range(total_cells), num_mines)
    mines = [(idx // GRID_SIZE, idx % GRID_SIZE) for idx in mines_indices]
    return grid, mines


def generate_keyboard(grid, game_id, player_id, safe_opened, mine_hits, num_mines):
    """Generate game board keyboard."""
    keyboard = []
    for i in range(GRID_SIZE):
        row = []
        for j in range(GRID_SIZE):
            val = grid[i][j]
            if val == 1:
                row.append(InlineKeyboardButton("💎", callback_data=f"mine_{game_id}_{player_id}_{i}_{j}_opened"))
            elif val == 2:
                row.append(InlineKeyboardButton("💥", callback_data=f"mine_{game_id}_{player_id}_{i}_{j}_opened"))
            elif val == 3:
                row.append(InlineKeyboardButton("💣", callback_data=f"mine_{game_id}_{player_id}_{i}_{j}_opened"))
            elif val == 4:
                row.append(InlineKeyboardButton("✨", callback_data=f"mine_{game_id}_{player_id}_{i}_{j}_opened"))
            else:
                row.append(InlineKeyboardButton("❓", callback_data=f"mine_{game_id}_{player_id}_{i}_{j}"))
        keyboard.append(row)
    
    game_over = mine_hits >= 1
    if safe_opened > 0 and not game_over:
        mult = get_multiplier(num_mines, safe_opened)
        keyboard.append([InlineKeyboardButton(f"🌸 Claim ({mult}x)", callback_data=f"claim_{game_id}_{player_id}_{safe_opened}")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_random_character(user_id, safe_opened):
    """Get random character reward."""
    characters_collection = get_collection("characters")
    
    if safe_opened < 6:
        rarities = ['⚪️ Common', '🟣 Rare', '🟢 Medium', '🟡 Legendary']
    else:
        rarities = ['💮 Special Edition', '🔮 Limited Edition', '💸 Premium Edition', '🎐 Celestial']
    
    pipeline = [
        {'$match': {'rarity': {'$in': rarities}, 'img_url': {'$exists': True, '$ne': ''}}},
        {'$sample': {'size': 1}}
    ]
    cursor = characters_collection.aggregate(pipeline)
    chars = await cursor.to_list(length=1)
    return chars[0] if chars else None


# Game state
game_state = {}
processing_locks = set()


@router.message(Command("mines"))
async def start_mines(message: Message) -> None:
    """Start a minesweeper game."""
    user_id = message.from_user.id
    args = message.text.split()
    
    bet = 1000
    num_mines = 3
    
    if len(args) > 1:
        try:
            bet = int(args[1])
        except ValueError:
            await message.reply("❌ Bet must be a number!", parse_mode=ParseMode.HTML)
            return
    
    if len(args) > 2:
        try:
            num_mines = int(args[2])
        except ValueError:
            await message.reply("❌ Mines count must be a number!", parse_mode=ParseMode.HTML)
            return
    
    if bet < MIN_BET or bet > MAX_BET:
        await message.reply(f"❌ Bet must be between {MIN_BET} and {MAX_BET}!", parse_mode=ParseMode.HTML)
        return
    
    if num_mines < MIN_MINES or num_mines > MAX_MINES:
        await message.reply(f"❌ Mines must be between {MIN_MINES} and {MAX_MINES}!", parse_mode=ParseMode.HTML)
        return
    
    balance = await get_user_balance(user_id)
    if balance < bet:
        await message.reply(f"❌ Insufficient balance! You have {balance}.", parse_mode=ParseMode.HTML)
        return
    
    await add_balance(user_id, -bet)
    
    game_id = str(uuid.uuid4())
    grid, mines = create_game(num_mines)
    
    game_state[user_id] = {
        'grid': grid, 'mines': mines, 'game_id': game_id,
        'safe_opened': 0, 'mine_hits': 0, 'bet': bet, 'num_mines': num_mines
    }
    
    caption = (
        f"🎮 <b>Minesweeper Casino</b>\n"
        f"👤 Player: {message.from_user.first_name}\n"
        f"🌸 Bet: <code>{bet:,}</code> petals\n"
        f"💣 Mines: <code>{num_mines}</code>\n\n"
        "💎 Open safe cells to increase multiplier!\n"
        "⚠️ Hit a mine and lose your bet!"
    )
    
    await message.reply_photo(
        photo="https://files.catbox.moe/szew66.png",
        caption=caption,
        reply_markup=generate_keyboard(grid, game_id, str(user_id), 0, 0, num_mines),
        parse_mode=ParseMode.HTML
    )


@router.callback_query(lambda c: c.data.startswith("mine_"))
async def handle_mine_click(callback: CallbackQuery) -> None:
    """Handle mine click."""
    data = callback.data.split('_')
    game_id, player_id, x, y = data[1], data[2], int(data[3]), int(data[4])
    user_id = callback.from_user.id
    
    if str(user_id) != player_id:
        await callback.answer("Not your game!", show_alert=True)
        return
    
    if user_id not in game_state or game_state[user_id]['game_id'] != game_id:
        await callback.answer("Game expired!", show_alert=True)
        return
    
    state = game_state[user_id]
    grid, mines, safe_opened, mine_hits = state['grid'], state['mines'], state['safe_opened'], state['mine_hits']
    bet, num_mines = state['bet'], state['num_mines']
    
    if grid[x][y] in [1, 2]:
        await callback.answer("Already revealed!", show_alert=True)
        return
    
    # Hit mine
    if (x, y) in mines:
        state['mine_hits'] += 1
        grid[x][y] = 2
        
        # Reveal board
        for rx in range(GRID_SIZE):
            for ry in range(GRID_SIZE):
                if (rx, ry) in mines:
                    if grid[rx][ry] != 2:
                        grid[rx][ry] = 3
                else:
                    if grid[rx][ry] != 1:
                        grid[rx][ry] = 4
        
        await callback.message.edit_text(
            "💥 <b>BOOM! Game Over!</b>\n"
            f"You hit a mine! Lost {bet:,} petals.",
            reply_markup=generate_keyboard(grid, game_id, player_id, safe_opened, state['mine_hits'], num_mines),
            parse_mode=ParseMode.HTML
        )
        del game_state[user_id]
        return
    
    # Safe cell
    grid[x][y] = 1
    state['safe_opened'] += 1
    safe_opened = state['safe_opened']
    
    total_safes = (GRID_SIZE * GRID_SIZE) - num_mines
    if safe_opened >= total_safes:
        # Auto claim
        del game_state[user_id]
        mult = get_multiplier(num_mines, safe_opened)
        winnings = int(bet * mult)
        await add_balance(user_id, winnings)
        
        await callback.message.edit_text(
            f"🎉 <b>Perfect Board Clear!</b>\n"
            f"Multiplier: {mult}x\n"
            f"Won: <code>{winnings:,}</code> petals!",
            parse_mode=ParseMode.HTML
        )
        return
    
    mult = get_multiplier(num_mines, safe_opened)
    caption = f"💎 Safe cell opened!\nMultiplier: {mult}x\nValue: <code>{int(bet * mult):,}</code> petals"
    
    await callback.message.edit_text(
        caption,
        reply_markup=generate_keyboard(grid, game_id, player_id, safe_opened, state['mine_hits'], num_mines),
        parse_mode=ParseMode.HTML
    )


@router.callback_query(lambda c: c.data.startswith("claim_"))
async def handle_claim(callback: CallbackQuery) -> None:
    """Claim winnings."""
    data = callback.data.split('_')
    game_id, player_id, safe_opened = data[1], data[2], int(data[3])
    user_id = callback.from_user.id
    
    if str(user_id) != player_id:
        await callback.answer("Not your game!", show_alert=True)
        return
    
    if user_id not in game_state or game_state[user_id]['game_id'] != game_id:
        await callback.answer("Game expired!", show_alert=True)
        return
    
    state = game_state[user_id]
    bet, num_mines = state['bet'], state['num_mines']
    del game_state[user_id]
    
    mult = get_multiplier(num_mines, safe_opened)
    winnings = int(bet * mult)
    await add_balance(user_id, winnings)
    
    await callback.message.edit_text(
        f"🌸 <b>Claimed!</b>\n"
        f"Multiplier: {mult}x\n"
        f"Won: <code>{winnings:,}</code> petals!",
        parse_mode=ParseMode.HTML
    )
