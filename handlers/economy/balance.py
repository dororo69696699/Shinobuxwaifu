# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# Rewritten with Clean Architecture
# ==========================================

"""
Balance and Economy Handlers

Handles:
- Daily rewards (/daily)
- Weekly rewards (/weekly)
- Balance check (/balance)
- Payments (/pay)
- Admin kill commands (/kill)
"""

import html
import logging
import time
from datetime import datetime, timedelta
from typing import Optional, Tuple

from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.core.config import Config
from app.database.repositories.user import UserRepository
from app.database.repositories.character import CharacterRepository
from app.services.permissions import PermissionService, Powers
from app.filters.admin import AdminOrVIPFilter, OwnerFilter
from app.utils.cooldown import CooldownManager

logger = logging.getLogger(__name__)

router = Router(name="balance")

# Cooldown manager
cooldown = CooldownManager(default_delay=2)


@router.message(Command("balance"))
async def balance_command(
    message: Message,
    user_repo: UserRepository,
    config: Config,
) -> None:
    """
    Handle /balance - Check user's balance.
    
    Args:
        message: Incoming message
        user_repo: User repository
        config: Bot configuration
    """
    user_id = message.from_user.id
    
    # Check cooldown
    if not cooldown.check(user_id, "balance", delay=2):
        return
    
    # Get balance
    user = await user_repo.get_by_id(user_id)
    balance = user.balance if user else 0
    tokens = user.tokens if user else 0
    
    user_name = html.escape(message.from_user.first_name)
    
    response = (
        f"🦋 <b>{user_name}'s Mansion Vault</b> 🌸\n\n"
        f"<blockquote>\n"
        f"━━━━━━━▧▣▧━━━━━━━\n"
        f"🌸 <b>Wisteria Petals:</b> {balance}\n"
        f"🎫 <b>Tokens:</b> {tokens}\n"
        f"━━━━━━━▧▣▧━━━━━━━\n"
        f"</blockquote>"
    )
    
    await message.reply(response, parse_mode="HTML")


@router.message(Command("daily"))
async def daily_command(
    message: Message,
    user_repo: UserRepository,
    config: Config,
) -> None:
    """
    Handle /daily - Claim daily reward.
    
    Args:
        message: Incoming message
        user_repo: User repository
        config: Bot configuration
    """
    user_id = message.from_user.id
    daily_amount = config.DAILY_REWARD or 100
    
    # Check cooldown
    if not cooldown.check(user_id, "daily", delay=5):
        await message.reply(
            "⏰ Ara ara~ Please wait before using this command again."
        )
        return
    
    # Check if already claimed today
    user = await user_repo.get_by_id(user_id)
    
    if user and user.last_daily:
        last_daily = user.last_daily
        if isinstance(last_daily, str):
            last_daily = datetime.fromisoformat(last_daily)
        
        today = datetime.now().date()
        if last_daily.date() == today:
            await message.reply(
                "🌸 Ara ara~ You have already claimed your daily Wisteria Petals today! "
                "Come back tomorrow."
            )
            return
    
    # Give daily reward
    await user_repo.add_balance(user_id, daily_amount)
    await user_repo.update_last_daily(user_id)
    
    new_balance = await user_repo.get_balance(user_id)
    user_name = html.escape(message.from_user.first_name)
    
    await message.reply(
        f"🦋 <b>Daily Wisteria Reward</b> 🌸\n\n"
        f"<blockquote>\n"
        f"Fufufu~ {user_name}, you received your daily Wisteria Petals!\n\n"
        f"🌸 <b>Reward:</b> +{daily_amount} Wisteria Petals\n"
        f"💳 <b>New Balance:</b> {new_balance} Wisteria Petals\n"
        f"</blockquote>",
        parse_mode="HTML",
    )


@router.message(Command("weekly"))
async def weekly_command(
    message: Message,
    user_repo: UserRepository,
    config: Config,
) -> None:
    """
    Handle /weekly - Claim weekly reward.
    
    Args:
        message: Incoming message
        user_repo: User repository
        config: Bot configuration
    """
    user_id = message.from_user.id
    weekly_amount = config.WEEKLY_REWARD or 2000
    
    # Check cooldown
    if not cooldown.check(user_id, "weekly", delay=5):
        await message.reply(
            "⏰ Ara ara~ Please wait before using this command again."
        )
        return
    
    # Check if already claimed this week
    user = await user_repo.get_by_id(user_id)
    
    if user and user.last_weekly:
        last_weekly = user.last_weekly
        if isinstance(last_weekly, str):
            last_weekly = datetime.fromisoformat(last_weekly)
        
        now = datetime.now()
        week_start = now - timedelta(days=now.weekday())
        week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
        
        if last_weekly >= week_start:
            next_week = week_start + timedelta(days=7)
            days_left = (next_week - now).days
            await message.reply(
                f"🌸 Ara ara~ You have already claimed your weekly Wisteria Petals! "
                f"Next gift available in {days_left} days."
            )
            return
    
    # Give weekly reward
    await user_repo.add_balance(user_id, weekly_amount)
    await user_repo.update_last_weekly(user_id)
    
    new_balance = await user_repo.get_balance(user_id)
    user_name = html.escape(message.from_user.first_name)
    
    await message.reply(
        f"🦋 <b>Weekly Wisteria Reward</b> 🎉\n\n"
        f"<blockquote>\n"
        f"Fufufu~ {user_name}, you received your weekly Wisteria Petals!\n\n"
        f"🌸 <b>Reward:</b> +{weekly_amount} Wisteria Petals\n"
        f"💳 <b>New Balance:</b> {new_balance} Wisteria Petals\n"
        f"</blockquote>",
        parse_mode="HTML",
    )


@router.message(Command("pay"))
async def pay_command(
    message: Message,
    user_repo: UserRepository,
    config: Config,
) -> None:
    """
    Handle /pay - Send coins to another user.
    
    Args:
        message: Incoming message
        user_repo: User repository
        config: Bot configuration
    """
    sender_id = message.from_user.id
    args = message.text.split()
    
    # Check cooldown
    if not cooldown.check(sender_id, "pay", delay=3):
        await message.reply(
            "⏰ Ara ara~ Please wait before sending another payment."
        )
        return
    
    # Parse amount
    if len(args) < 2:
        await message.reply(
            "🦋 <b>Usage:</b> /pay <amount> [@username/user_id] or reply to a user."
        )
        return
    
    try:
        amount = int(args[1])
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.reply(
            "❌ Invalid amount. Please enter a positive number."
        )
        return
    
    # Find recipient
    recipient_id = None
    recipient_name = None
    
    if message.reply_to_message:
        recipient_id = message.reply_to_message.from_user.id
        recipient_name = message.reply_to_message.from_user.first_name
    elif len(args) > 2:
        try:
            recipient_id = int(args[2])
        except ValueError:
            username = args[2].lstrip('@')
            user = await user_repo.get_by_username(username)
            if user:
                recipient_id = user.id
                recipient_name = user.first_name
            else:
                await message.reply(
                    "❌ Recipient not found. Please check the username."
                )
                return
    
    if not recipient_id:
        await message.reply(
            "❌ Recipient not found. Reply to a user or provide a valid user ID/username."
        )
        return
    
    # Check sender balance
    sender_balance = await user_repo.get_balance(sender_id)
    if sender_balance < amount:
        await message.reply(
            "❌ Insufficient Wisteria Petals."
        )
        return
    
    # Transfer coins
    await user_repo.add_balance(sender_id, -amount)
    await user_repo.add_balance(recipient_id, amount)
    
    new_sender_balance = await user_repo.get_balance(sender_id)
    
    sender_name = html.escape(message.from_user.first_name or str(sender_id))
    recipient_display = html.escape(recipient_name or str(recipient_id))
    
    # Notify sender
    await message.reply(
        f"🦋 <b>Payment Successful</b> 🌸\n\n"
        f"<blockquote>\n"
        f"✅ You paid {amount} Wisteria Petals to {recipient_display}\n\n"
        f"💳 <b>Your New Balance:</b> {new_sender_balance} Wisteria Petals\n"
        f"</blockquote>",
        parse_mode="HTML",
    )
    
    # Notify recipient
    try:
        await message.bot.send_message(
            chat_id=recipient_id,
            text=(
                f"🦋 <b>Payment Received</b> 🎉\n\n"
                f"<blockquote>\n"
                f"🌸 You received {amount} Wisteria Petals from {sender_name}!\n"
                f"</blockquote>"
            ),
            parse_mode="HTML",
        )
    except Exception as e:
        logger.warning(f"Could not notify recipient {recipient_id}: {e}")


@router.message(Command("kill"), AdminOrVIPFilter())
async def kill_command(
    message: Message,
    user_repo: UserRepository,
    character_repo: CharacterRepository,
    config: Config,
) -> None:
    """
    Handle /kill - Admin/VIP command to manage user data.
    
    Args:
        message: Incoming message
        user_repo: User repository
        character_repo: Character repository
        config: Bot configuration
    """
    args = message.text.split()
    
    # Check if replying to a user
    if not message.reply_to_message:
        await message.reply(
            "🦋 Please reply to a user's message to use the /kill command."
        )
        return
    
    user_id = message.reply_to_message.from_user.id
    
    if len(args) < 2:
        await message.reply(
            "🧪 <b>Kill Command Usage:</b>\n\n"
            "<blockquote>\n"
            "• <code>c</code> ➜ Delete character\n"
            "• <code>f</code> ➜ Delete full data\n"
            "• <code>b [amount]</code> ➜ Deduct balance\n"
            "</blockquote>",
            parse_mode="HTML",
        )
        return
    
    option = args[1]
    
    try:
        if option == 'f':
            # Delete full user data
            await user_repo.delete(user_id)
            await message.reply(
                "🦋 <b>Data Erased</b>\n\n"
                "<blockquote>\n"
                "The full data of the user has been deleted from the mansion records.\n"
                "</blockquote>",
                parse_mode="HTML",
            )
            
        elif option == 'c':
            # Delete specific character
            if len(args) < 3:
                await message.reply(
                    "🦋 Please specify a character ID to remove."
                )
                return
            
            char_id = args[2]
            user = await user_repo.get_by_id(user_id)
            
            if user and user.characters:
                char_ids = user.characters
                if char_id in char_ids:
                    char_ids.remove(char_id)
                    await user_repo.update_characters(user_id, char_ids)
                    await message.reply(
                        f"🦋 <b>Character Removed</b>\n\n"
                        f"<blockquote>\n"
                        f"Character with ID {char_id} has been removed from the collection.\n"
                        f"</blockquote>",
                        parse_mode="HTML",
                    )
                else:
                    await message.reply(
                        f"❌ No character with ID {char_id} found in the user's collection."
                    )
            else:
                await message.reply(
                    "❌ No characters found in the user's collection."
                )
                
        elif option == 'b':
            # Deduct balance
            if len(args) < 3:
                await message.reply(
                    "🦋 Please specify an amount to deduct from balance."
                )
                return
            
            try:
                amount = int(args[2])
                if amount <= 0:
                    raise ValueError
            except ValueError:
                await message.reply(
                    "❌ Invalid amount. Please enter a positive number."
                )
                return
            
            current_balance = await user_repo.get_balance(user_id)
            new_balance = max(0, current_balance - amount)
            
            await user_repo.set_balance(user_id, new_balance)
            await message.reply(
                f"🦋 <b>Balance Deducted</b>\n\n"
                f"<blockquote>\n"
                f"{amount} Wisteria Petals have been deducted.\n\n"
                f"💳 <b>New Balance:</b> {new_balance} Wisteria Petals\n"
                f"</blockquote>",
                parse_mode="HTML",
            )
            
        else:
            await message.reply(
                "❌ <b>Invalid Option</b>\n\n"
                "<blockquote>\n"
                "Use <code>c</code> for character, <code>f</code> for full data, "
                "or <code>b [amount]</code> to deduct balance.\n"
                "</blockquote>",
                parse_mode="HTML",
            )
            
    except Exception as e:
        logger.error(f"Error in /kill command: {e}")
        await message.reply(
            "❌ An error occurred while processing the request. Please try again later."
        )
