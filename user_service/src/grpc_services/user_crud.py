from user_service.src.db.database import Database
from user_service.src.db.models import User
from sqlalchemy.future import select
from sqlalchemy import update, delete
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


class UserCrud:
    def __init__(self, db: Database):
        self.db = db

    async def read(self, user_id: int):
        try:
            async with self.db.session_scope() as session:
                user = await session.scalar(select(User).where(User.id == user_id))
                return user
        except SQLAlchemyError as e:
            raise e
        # How to handle this on server side?

    async def create(self, user):
        try:
            async with self.db.session_scope() as session:
                user_db = User(
                    username=user.username,
                    email=user.email,
                    password=user.password,
                )
                session.add(user_db)
                return "success"
        except (IntegrityError, SQLAlchemyError) as e:
            raise e

    async def update_password(self, user_id: int, new_password: str):
        try:
            async with self.db.session_scope() as session:
                await session.execute(
                    update(User).values(password=new_password).where(User.id == user_id)
                )
        except SQLAlchemyError as e:
            raise e

    async def delete(self, user_id: int):
        try:
            async with self.db.session_scope() as session:
                await session.execute(delete(User).where(User.id == user_id))
        except SQLAlchemyError as e:
            raise e


    async def get_user_by_email(self, user_email: str):
        try:
            async with self.db.session_scope() as session:
                user = await session.scalar(select(User).where(User.email == user_email))
                return user
        except SQLAlchemyError as e:
            raise e
