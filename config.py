import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Hardcoded API credentials to make the bot deployable with only BOT_TOKEN
# These are standard credentials and do not need to be changed by the user.
API_ID = 25055319
API_HASH = "b082725e172a8c3d79040d85a1112461"

if not BOT_TOKEN:
    print("❌ ERROR: BOT_TOKEN is missing in environment variables!")

# Admin Configuration
try:
    ADMIN_ID = int(os.getenv("ADMIN_ID", "6612030110"))
except ValueError:
    print("⚠️ WARNING: ADMIN_ID in environment is not a valid integer. Using default.")
    ADMIN_ID = 6612030110

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin_username")

# Database Configuration
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "ReferralBot")

# Force Join Configuration (Space-separated usernames)
FSUB_CHANNELS = os.getenv("FSUB_CHANNELS", "@Thealphabotz").split()

# Referral Configuration
try:
    REDEEM_THRESHOLD = int(os.getenv("REDEEM_THRESHOLD", "5"))
except ValueError:
    REDEEM_THRESHOLD = 5

# Web Server Configuration
WEB_SERVER = os.getenv("WEB_SERVER", "True").lower() == "true"
PING_URL = os.getenv("PING_URL")
try:
    PING_TIME = int(os.getenv("PING_TIME", "600"))
except ValueError:
    PING_TIME = 600

class Messages:
    START_TEXT = (
        "👋 **Welcome to the Referral Bot!**\n\n"
        "Earn points by inviting your friends and redeem them for exciting rewards!\n\n"
        "📢 **Join our channels to get started.**"
    )

    FORCE_JOIN_TEXT = (
        "⚠️ **Access Denied!**\n\n"
        "You must join the following channels to use this bot:\n\n"
        "{channels}\n\n"
        "After joining, click the **Verify** button below."
    )

    MAIN_MENU_TEXT = (
        "🎊 **Welcome back, {user_name}!**\n\n"
        "Your current points: `{points}`\n"
        "Milestone for redemption: `{threshold}` points\n\n"
        "Use the buttons below to manage your referrals."
    )

    REFERRAL_TEXT = (
        "🔗 **Your Unique Referral Link:**\n"
        "`{link}`\n\n"
        "Share this link with your friends. You get **1 point** for every friend who joins and verifies!"
    )

    REDEEM_SUCCESS_USER = (
        "✅ **Redemption Request Sent!**\n\n"
        "You have reached the milestone. Your request has been sent to the admin.\n"
        "Click the button below to contact the admin for your reward."
    )

    REDEEM_SUCCESS_ADMIN = (
        "🔔 **New Redemption Request!**\n\n"
        "User: {user_mention} (`{user_id}`)\n"
        "Points: `{points}`"
    )

    ALREADY_VERIFIED = "✅ You are already verified!"
    NOT_JOINED_ALL = "❌ You haven't joined all channels yet!"
    NOT_ENOUGH_POINTS = "❌ You need at least {threshold} points to redeem. Currently you have {points} points."
