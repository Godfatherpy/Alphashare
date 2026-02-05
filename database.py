from motor.motor_asyncio import AsyncIOMotorClient
import config
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        try:
            self.client = AsyncIOMotorClient(config.MONGO_URI)
            self.db = self.client[config.DATABASE_NAME]
            self.users = self.db.users
            logger.info("Connected to MongoDB")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")

    async def add_user(self, user_id, username=None, first_name=None, referred_by=None):
        user = await self.users.find_one({"user_id": user_id})
        if not user:
            user_data = {
                "user_id": user_id,
                "username": username,
                "first_name": first_name,
                "points": 0,
                "referred_by": referred_by,
                "is_verified": False,
                "point_awarded": False,
                "join_date": datetime.now()
            }
            await self.users.insert_one(user_data)
            logger.info(f"New user added: {user_id}")
            return True
        return False

    async def get_user(self, user_id):
        return await self.users.find_one({"user_id": user_id})

    async def increment_points(self, user_id):
        await self.users.update_one(
            {"user_id": user_id},
            {"$inc": {"points": 1}}
        )
        logger.info(f"Incremented points for user: {user_id}")

    async def set_verified(self, user_id):
        await self.users.update_one(
            {"user_id": user_id},
            {"$set": {"is_verified": True}}
        )
        logger.info(f"User verified: {user_id}")

    async def set_point_awarded(self, user_id):
        await self.users.update_one(
            {"user_id": user_id},
            {"$set": {"point_awarded": True}}
        )
        logger.info(f"Point awarded status set for user: {user_id}")

    async def get_total_users_count(self):
        return await self.users.count_documents({})
