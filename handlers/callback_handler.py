from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config
from helper_func import is_subscribed

@Client.on_callback_query()
async def callback_handler(bot, query):
    user_id = query.from_user.id
    data = query.data

    if data == "verify":
        if await is_subscribed(bot, user_id):
            await query.answer(config.Messages.ALREADY_VERIFIED, show_alert=True)
            user_data = await bot.db.get_user(user_id)
            if not user_data.get("is_verified"):
                await bot.db.set_verified(user_id)
                if user_data.get("referred_by") and not user_data.get("point_awarded"):
                    await bot.db.increment_points(user_data["referred_by"])
                    await bot.db.set_point_awarded(user_id)
                    try:
                        await bot.send_message(user_data["referred_by"], "🎊 **Someone joined using your link! You got 1 point.**")
                    except Exception as e:
                        print(f"Could not notify referrer {user_data['referred_by']}: {e}")
                user_data = await bot.db.get_user(user_id)
            
            # Show main menu
            buttons = [
                [InlineKeyboardButton("🔗 Referral Link", callback_data="ref_link")],
                [InlineKeyboardButton("📊 My Stats", callback_data="stats"), InlineKeyboardButton("🎁 Redeem", callback_data="redeem")]
            ]
            await query.message.edit_text(
                config.Messages.MAIN_MENU_TEXT.format(
                    user_name=user_data.get("first_name") or "User",
                    points=user_data.get("points", 0),
                    threshold=config.REDEEM_THRESHOLD
                ),
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        else:
            await query.answer(config.Messages.NOT_JOINED_ALL, show_alert=True)

    elif data == "ref_link":
        bot_me = await bot.get_me()
        link = f"https://t.me/{bot_me.username}?start={user_id}"
        await query.message.edit_text(
            config.Messages.REFERRAL_TEXT.format(link=link),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="home")]])
        )

    elif data == "stats":
        user_data = await bot.db.get_user(user_id)
        await query.answer(f"Your Points: {user_data.get('points', 0)}", show_alert=True)

    elif data == "redeem":
        user_data = await bot.db.get_user(user_id)
        points = user_data.get("points", 0)
        if points >= config.REDEEM_THRESHOLD:
            # Notify Admin
            try:
                await bot.send_message(
                    config.ADMIN_ID,
                    config.Messages.REDEEM_SUCCESS_ADMIN.format(
                        user_mention=query.from_user.mention,
                        user_id=user_id,
                        points=points
                    )
                )
            except Exception as e:
                print(f"Could not notify admin: {e}")
                
            # Notify User
            admin_username = config.ADMIN_USERNAME.replace('@', '')
            buttons = [[InlineKeyboardButton("👤 Contact Admin", url=f"https://t.me/{admin_username}")]]
            await query.message.edit_text(
                config.Messages.REDEEM_SUCCESS_USER,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        else:
            await query.answer(
                config.Messages.NOT_ENOUGH_POINTS.format(threshold=config.REDEEM_THRESHOLD, points=points),
                show_alert=True
            )

    elif data == "home":
        user_data = await bot.db.get_user(user_id)
        buttons = [
            [InlineKeyboardButton("🔗 Referral Link", callback_data="ref_link")],
            [InlineKeyboardButton("📊 My Stats", callback_data="stats"), InlineKeyboardButton("🎁 Redeem", callback_data="redeem")]
        ]
        await query.message.edit_text(
            config.Messages.MAIN_MENU_TEXT.format(
                user_name=user_data.get("first_name") or "User",
                points=user_data.get("points", 0),
                threshold=config.REDEEM_THRESHOLD
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
