# Run: python -m scripts.seed_cosmetics
import asyncio
from sqlalchemy import text, select
from app.db.session import engine, Base

from app.db.session import async_session_factory
from app.models.pet_cosmetic import PetCosmetic
from app.data.cosmetic_catalog import COSMETIC_CATALOG

async def drop_table():
    async with engine.begin() as conn:
        await conn.execute(text("DROP TABLE IF EXISTS pet_cosmetic"))

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
async def seed():

    async with async_session_factory() as db:

        for cosmetic in COSMETIC_CATALOG:

            result = await db.execute(
                select(PetCosmetic).where(PetCosmetic.name == cosmetic["name"])
            )

            exists = result.scalar_one_or_none()

            if exists:
                continue

            item = PetCosmetic(**cosmetic)
            db.add(item)

        await db.commit()

    print("Cosmetics seeded")

asyncio.run(drop_table())
asyncio.run(create_tables())
asyncio.run(seed())