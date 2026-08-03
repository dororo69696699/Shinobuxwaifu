import random
import time
from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.enums import ParseMode

from database.models import get_user, add_balance, get_collection

router = Router(name="tictactoe")

games_collection = get_collection("ox_games")
stats_collection = get_collection("ox_stats")

MIN_BET = 100
MAX_BET = 100000


def check_winner(board):
    for r in range(3):
        if board[r][0] != "" and board[r][0] == board[r][1] == board[r][2]:
            return board[r][0]
    for c in range(3):
        if board[0][c] != "" and board[0][c] == board[1][c] == board[2][c]:
            return board[0][c]
    if board[0][0] != "" and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] != "" and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    return None


def is_board_full(board):
    return all(cell != "" for row in board for cell in row)


def make_board_keyboard(game_id: str, board: list) -> InlineKeyboardMarkup:
    keyboard = []
    for r in range(3):
        row = []
        for c in range(3):
            val = board[r][c]
            emoji = "❌" if val == "X" else ("⭕" if val == "O" else "⬜")
            row.append(InlineKeyboardButton(emoji, callback_data=f"ox_play_{game_id}_{r}_{c}"))
        keyboard.append(row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@router.message(Command("ox"))
async def host_ox_game(message: Message) -> None:
    user_id = message.from_user.id
    args = message.text.split()
    
    if len(args) < 2:
        await message.reply("Usage: <code>/ox &lt;bet&gt;</code>", parse_mode=ParseMode.HTML)
        return
    
    try:
        bet = int(args[1])
    except ValueError:
        await message.reply("❌ Bet must be a number!", parse_mode=ParseMode.HTML)
        return
    
    if bet < MIN_BET or bet > MAX_BET:
        await message.reply(f"❌ Bet must be between {MIN_BET:,} and {MAX_BET:,}!", parse_mode=ParseMode.HTML)
        return
    
    existing = await games_collection.find_one({
        "status": {"$in": ["lobby", "playing"]},
        "$or": [{"player1": user_id}, {"player2": user_id}]
    })
    if existing:
        await message.reply("❌ You already have an active game!", parse_mode=ParseMode.HTML)
        return
    
    user = await get_user(user_id)
    balance = user.get("balance", 0) if user else 0
    if balance < bet:
        await message.reply(f"❌ Insufficient balance! You have {balance:,}.", parse_mode=ParseMode.HTML)
        return
    
    await add_balance(user_id, -bet)
    game_id = str(int(time.time() * 1000))
    game_data = {
        "game_id": game_id,
        "player1": user_id,
        "player1_name": message.from_user.first_name,
        "player2": None,
        "player2_name": None,
        "bet": bet,
        "prize_pool": bet * 2,
        "symbol_x": None,
        "symbol_o": None,
        "turn": None,
        "board": [["", "", ""], ["", "", ""], ["", "", ""]],
        "status": "lobby",
        "created_at": time.time(),
        "last_move_at": time.time(),
        "chat_id": message.chat.id,
        "message_id": None
    }
    await games_collection.insert_one(game_data)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("🎮 Join Game", callback_data=f"join_ox_{game_id}")],
        [InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_ox_{game_id}")]
    ])
    
    sent = await message.reply(
        f"🎮 <b>Tic Tac Toe</b>\n\nHost: {message.from_user.first_name}\nBet: <code>{bet:,}</code> petals\n\n⏳ Waiting for opponent...",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )
    await games_collection.update_one({"game_id": game_id}, {"$set": {"message_id": sent.message_id}})


@router.callback_query(lambda c: c.data and c.data.startswith("join_ox_"))
async def join_ox_callback(callback: CallbackQuery) -> None:
    game_id = callback.data.split("_")[2]
    user_id = callback.from_user.id
    
    game = await games_collection.find_one({"game_id": game_id})
    if not game or game["status"] != "lobby":
        await callback.answer("Game not available!", show_alert=True)
        return
    
    if game["player1"] == user_id:
        await callback.answer("You can't join your own game!", show_alert=True)
        return
    
    user = await get_user(user_id)
    balance = user.get("balance", 0) if user else 0
    if balance < game["bet"]:
        await callback.answer(f"Insufficient! Need {game['bet']:,} petals.", show_alert=True)
        return
    
    await add_balance(user_id, -game["bet"])
    players = [game["player1"], user_id]
    random.shuffle(players)
    
    await games_collection.update_one(
        {"game_id": game_id},
        {
            "$set": {
                "player2": user_id,
                "player2_name": callback.from_user.first_name,
                "symbol_x": players[0],
                "symbol_o": players[1],
                "turn": random.choice(players),
                "status": "playing",
                "last_move_at": time.time()
            }
        }
    )
    
    game = await games_collection.find_one({"game_id": game_id})
    p1_symbol = "❌" if game["symbol_x"] == game["player1"] else "⭕"
    p2_symbol = "❌" if game["symbol_x"] == game["player2"] else "⭕"
    turn_name = game["player1_name"] if game["turn"] == game["player1"] else game["player2_name"]
    turn_symbol = "❌" if game["symbol_x"] == game["turn"] else "⭕"
    
    caption = (
        f"🎮 <b>Tic Tac Toe</b>\n{p1_symbol} {game['player1_name']}\n{p2_symbol} {game['player2_name']}\n\n"
        f"Prize: <code>{game['prize_pool']:,}</code> petals\nTurn: {turn_name} ({turn_symbol})"
    )
    
    await callback.message.edit_text(caption, reply_markup=make_board_keyboard(game_id, game["board"]), parse_mode=ParseMode.HTML)
    await callback.answer("Game started!")


@router.callback_query(lambda c: c.data and c.data.startswith("cancel_ox_"))
async def cancel_ox_callback(callback: CallbackQuery) -> None:
    game_id = callback.data.split("_")[2]
    user_id = callback.from_user.id
    
    game = await games_collection.find_one({"game_id": game_id})
    if not game or game["player1"] != user_id:
        await callback.answer("Only host can cancel!", show_alert=True)
        return
    
    await add_balance(user_id, game["bet"])
    await games_collection.update_one({"game_id": game_id}, {"$set": {"status": "cancelled"}})
    await callback.message.edit_text("❌ Game cancelled. Refunded host.")
    await callback.answer("Cancelled.")


@router.callback_query(lambda c: c.data and c.data.startswith("ox_play_"))
async def play_ox_callback(callback: CallbackQuery) -> None:
    data = callback.data.split("_")
    game_id, row, col = data[2], int(data[3]), int(data[4])
    user_id = callback.from_user.id
    
    game = await games_collection.find_one({"game_id": game_id})
    if not game or game["status"] != "playing":
        await callback.answer("Game ended!", show_alert=True)
        return
    
    if user_id not in (game["player1"], game["player2"]):
        await callback.answer("Not your game!", show_alert=True)
        return
    
    if user_id != game["turn"]:
        await callback.answer("Not your turn!", show_alert=True)
        return
    
    board = game["board"]
    if board[row][col] != "":
        await callback.answer("Cell already taken!", show_alert=True)
        return
    
    symbol = "X" if game["symbol_x"] == user_id else "O"
    board[row][col] = symbol
    winner = check_winner(board)
    
    if winner:
        winner_id = game["symbol_x"] if winner == "X" else game["symbol_o"]
        await games_collection.update_one({"game_id": game_id}, {"$set": {"board": board, "status": "ended", "winner": winner_id}})
        await add_balance(winner_id, game["prize_pool"])
        winner_name = game["player1_name"] if winner_id == game["player1"] else game["player2_name"]
        await callback.message.edit_text(
            f"🏆 <b>{winner_name} Won!</b>\nPrize: <code>{game['prize_pool']:,}</code> petals",
            reply_markup=make_board_keyboard(game_id, board),
            parse_mode=ParseMode.HTML
        )
        await callback.answer(f"{winner_name} won!")
        return
    elif is_board_full(board):
        await games_collection.update_one({"game_id": game_id}, {"$set": {"board": board, "status": "ended"}})
        await add_balance(game["player1"], game["bet"])
        await add_balance(game["player2"], game["bet"])
        await callback.message.edit_text(
            "🤝 <b>Draw!</b>\nBoth players refunded.",
            reply_markup=make_board_keyboard(game_id, board),
            parse_mode=ParseMode.HTML
        )
        await callback.answer("Draw!")
        return
    
    next_turn = game["player2"] if game["turn"] == game["player1"] else game["player1"]
    await games_collection.update_one({"game_id": game_id}, {"$set": {"board": board, "turn": next_turn, "last_move_at": time.time()}})
    
    game = await games_collection.find_one({"game_id": game_id})
    turn_name = game["player1_name"] if game["turn"] == game["player1"] else game["player2_name"]
    turn_symbol = "❌" if game["symbol_x"] == game["turn"] else "⭕"
    caption = (
        f"🎮 <b>Tic Tac Toe</b>\n❌ {game['player1_name']}\n⭕ {game['player2_name']}\n\n"
        f"Prize: <code>{game['prize_pool']:,}</code> petals\nTurn: {turn_name} ({turn_symbol})"
    )
    await callback.message.edit_text(caption, reply_markup=make_board_keyboard(game_id, board), parse_mode=ParseMode.HTML)
    await callback.answer()
