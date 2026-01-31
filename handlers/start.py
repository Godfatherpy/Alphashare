from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config
from helper_func import is_subscribed

@Client.on_message(filters.command("start") & filters.private)
async def start_handler(bot, message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name

    # Check for referral parameter
    referred_by = None
    if len(message.command) > 1:
        try:
            referred_by = int(message.command[1])
            if referred_by == user_id:
                referred_by = None # Can't refer yourself
        except:
            pass

    # Add user to DB
    await bot.db.add_user(user_id, username, first_name, referred_by)

    # Check if joined
    if not await is_subscribed(bot, user_id):
        # Show Force Join buttons
        buttons = []
        for channel in config.FSUB_CHANNELS:
            channel_link = channel.replace('@', '')
            buttons.append([InlineKeyboardButton(f"Join {channel}", url=f"https://t.me/{channel_link}")])
        buttons.append([InlineKeyboardButton("Verify ✅", callback_data="verify")])

        await message.reply_text(
            config.Messages.FORCE_JOIN_TEXT.format(channels="\n".join(config.FSUB_CHANNELS)),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return

    # If joined, show main menu
    user_data = await bot.db.get_user(user_id)
    # Also set verified if not already
    if not user_data.get("is_verified"):
        await bot.db.set_verified(user_id)
        # Handle referral point award if not already awarded
        if user_data.get("referred_by") and not user_data.get("point_awarded"):
            await bot.db.increment_points(user_data["referred_by"])
            await bot.db.set_point_awarded(user_id)
            try:
                await bot.send_message(user_data["referred_by"], "🎊 **Someone joined using your link! You got 1 point.**")
            except:
                pass
        user_data = await bot.db.get_user(user_id) # Refresh data

    await show_main_menu(message, user_data)

async def show_main_menu(message, user_data):
    buttons = [
        [InlineKeyboardButton("🔗 Referral Link", callback_data="ref_link")],
        [InlineKeyboardButton("📊 My Stats", callback_data="stats"), InlineKeyboardButton("🎁 Redeem", callback_data="redeem")]
    ]
    await message.reply_text(
        config.Messages.MAIN_MENU_TEXT.format(
            user_name=user_data.get("first_name") or "User",
            points=user_data.get("points", 0),
            threshold=config.REDEEM_THRESHOLD
        ),
        reply_markup=InlineKeyboardMarkup(buttons)
    )
