# Telegram Referral Bot

A robust Telegram bot built with Pyrogram and MongoDB that incentivizes user growth through a point-based referral system.

## Features
- **Mandatory Channel Join**: Restricts access until users join specified channels.
- **Referral System**: Unique referral links for every user.
- **Point System**: 1 Referral = 1 Point.
- **Redemption Workflow**: Users can redeem points once they hit a milestone, notifying the admin.
- **Web Server**: Built-in health check for deployment on Render/Koyeb.

## Setup
1. Clone the repo.
2. Fill in the `.env` file with your `API_ID`, `API_HASH`, `BOT_TOKEN`, and `MONGO_URI`.
3. Configure `FSUB_CHANNELS`, `ADMIN_ID`, and `REDEEM_THRESHOLD` in `config.py` or `.env`.
4. Run `python3 main.py`.

## Commands
- `/start`: Initiation and referral handling.
- Buttons for: Referral Link, My Stats, Redeem.
