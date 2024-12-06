from src.db.database import Database
from src.db.models import User
from sqlalchemy.future import select
from sqlalchemy import update, delete
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


class UserCrud:
    def __init__(self, db: Database):
        self.db=db

    async def read(self, user_id: int):
        try:
            db = await self.db.get_db()
            user = await db.scalar(select(User).where(User.id == user_id))
            return user
        except SQLAlchemyError:
            raise
        # How to handle this on server side?

    async def create(self, user):
        db = await self.get_db()
        try:
            user_db = User(
                username=user.username,
                email=user.email,
                password=user.password,
            )
            db.add(user_db)
            await db.commit()
            await db.refresh(user_db)
            return "success"
        except IntegrityError:
            await db.rollback()
            return "Account already exists with this username/email."
        except SQLAlchemyError:
            raise

    async def update_password(self, user_id: int, new_password: str):
        try:
            db = await self.get_db()
            await db.execute(
                update(User).values(password=new_password).where(User.id == user_id)
            )
            await db.commit()
        except SQLAlchemyError:
            raise

    async def delete(self, user_id: int):
        try:
            db = await self.get_db()
            await db.execute(delete(User).where(User.id == user_id))
            await db.commit()
        except SQLAlchemyError:
            raise