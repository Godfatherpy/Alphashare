import config
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, ChatWriteForbidden

async def is_subscribed(bot, user_id):
    if not config.FSUB_CHANNELS:
        return True

    for channel in config.FSUB_CHANNELS:
        try:
            member = await bot.get_chat_member(channel, user_id)
            if member.status in ["kicked", "left"]:
                return False
        except UserNotParticipant:
            return False
        except (ChatAdminRequired, ChatWriteForbidden):
            print(f"⚠️ Bot is not admin in {channel}!")
            continue
        except Exception as e:
            print(f"Error checking sub for {channel}: {e}")
            continue
    return True
