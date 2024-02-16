import asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncAttrs, AsyncSession, create_async_engine
from config import Config, load_config
from db_base import Base
from  models import User


class DBConnection:
    @staticmethod
    async def create_db_session(config: Config):
        engine = create_async_engine(DBConnection.make_connection_string(config), echo=True)
        return engine

    @staticmethod
    def make_connection_string(config: Config) -> str:
        result = f"mysql+asyncmy://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.database}"
        return result

    @staticmethod
    async def main():
        config = load_config('.env')
        engine = await DBConnection.create_db_session(config)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)



