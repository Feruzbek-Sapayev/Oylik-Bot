from app.database.models import User
from app.database.models import async_session

from sqlalchemy import select, insert, update


async def select_user(telegram_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == telegram_id))
        return user

async def add_user(telegram_id, phone_number, jshshir):
    async with async_session() as session:
        user = session.add(User(telegram_id=telegram_id, phone_number=phone_number, jshshir=jshshir))
        await session.commit()  
        return user

async def update_user_phone(telegram_id, phone_number):
    async with async_session() as session:
        async with session.begin():
            sql = update(User).where(User.telegram_id == telegram_id).values(phone_number=phone_number)
            await session.execute(sql)
            await session.commit()  
    
async def update_user_jshshir(telegram_id, jshshir):
    async with async_session() as session:
        async with session.begin():
            sql = update(User).where(User.telegram_id == telegram_id).values(jshshir=jshshir).execution_options(synchronize_session="fetch")
            await session.execute(sql)
            await session.commit()  