import asyncio

from data.config import load_config
from db_api.init_db import DBConnection
from db_api.database import SQLAlchemySession

config = load_config(path='.env')
async def create_tables():
    await DBConnection.main()


Database: SQLAlchemySession = SQLAlchemySession(f"mysql+asyncmy://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.database}")

async def test_database():
    await Database.add_user(324456)
    count = await Database.count_user()
    all_user = await Database.select_all_user()
    print(all_user)
    print(count)

async def main():
    await create_tables()

if __name__ == "__main__":
    asyncio.run(main())