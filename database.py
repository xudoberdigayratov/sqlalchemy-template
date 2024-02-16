import asyncio
from datetime import timedelta, datetime

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from config import Config, load_config
from sqlalchemy import select, func, update
from models import User
from typing import Optional


config = load_config('.env')

class SQLAlchemySession():
    def __init__(self, SQLALCHEMY_DATABASE_URI):
        self.engine = create_async_engine(SQLALCHEMY_DATABASE_URI, echo=True)
        self.async_session_maker = async_sessionmaker(bind=self.engine, expire_on_commit=False)

    async def get_user(self, user_id: int) -> User | None:
        async with self.async_session_maker() as session:
            query = select(User).where(User.user_id == user_id)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            return user

    async def update_user(self, user_id: int, status: str) -> User | None:
        try:
            async with self.async_session_maker() as session:
                query = update(User).where(User.user_id == user_id).values(status=status).execution_options(synchronize_session="fetch")
                await session.execute(query)
                await session.commit()
                return await self.get_user(user_id)
        except Exception as err:
            print(f"Error occurred while updating user: {err}")

    async def add_user(self, user_id: int) -> None:
        try:
            async with self.async_session_maker() as session:
                user: Optional[User] = await self.get_user(user_id)
                if user is None:
                    new_user = User(user_id=user_id)
                    session.add(new_user)
                    await session.commit()
                    return dict(status=new_user.status, user_id=new_user.user_id)
                else:
                    if user.status == 'passive':
                        updated_user: Optional[User] = await self.update_user(user_id=user_id, status='active')
                        return dict(status=updated_user.status, user_id=updated_user.user_id)
                    return dict(status=user.status, user_id=user.user_id)
        except Exception as err:
            print(err)

    async def select_all_user(self):
        async with self.async_session_maker() as session:
            query = select('*').select_from(User)
            result = await session.execute(query)
            return result.fetchall()

    async def count_user(self):
        async with self.async_session_maker() as session:
            query = select(func.count()).select_from(User)
            result = await session.execute(query)
            count = result.scalar()
            return count

    async def count_user_one_month(self):
        async with self.async_session_maker() as session:
            start_date = datetime.now() - timedelta(days=30)
            end_date = datetime.now() + timedelta(days=1)
            query = select(func.count(User.id)).where(User.created_at >= start_date, User.created_at < end_date)
            result = await session.execute(query)
            count = result.scalar()
            return count

    async def count_user_one_now(self):
        async with self.async_session_maker() as session:
            current_date = datetime.now().date()
            query = select(func.count(User.id)).where(func.DATE(User.created_at) == current_date)
            result = await session.execute(query)
            count = result.scalar()
            return count



