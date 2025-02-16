from user_service.src.db.database import Database
from user_service.src.db.models import User
from sqlalchemy.future import select
from sqlalchemy import update, delete
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List


class UserCrud:
    def __init__(self, db: Database):
        self.db = db

    async def get_user(self, user_id: int):
        try:
            async with self.db.session_scope() as session:
                user = await session.scalar(select(User).where(User.id == user_id))
                return user
        except SQLAlchemyError as e:
            raise e
        # How to handle this on server side?

    async def create_user(self, user):
        try:
            async with self.db.session_scope() as session:
                user_db = User(
                    username=user.username,
                    email=user.email,
                    password=user.password,
                )
                session.add(user_db)
                await session.flush()
                print(f'new user is{user_db}')
                print(f"the user id: {user_db.id}")
                return user_db.id
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

    async def delete_user(self, user_id: int):
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


    async def get_user_emails(self, ids: List[int]):
        try:
            async with self.db.session_scope() as session:
                stmt = select(User).filter(User.id.in_(ids))
                result = await session.execute(stmt)
                users = result.scalars().all()
                emails = [user.email for user in users]
                return emails
        except SQLAlchemyError as e:
            raise e