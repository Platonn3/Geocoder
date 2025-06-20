from Source.database.models import async_session, Address
from sqlalchemy import select


async def return_address_if_exist(query: str):
    async with async_session() as session:
        result = await session.execute(
            select(Address)
            .where(Address.input_query == query)
        )
        return result.scalar_one_or_none()


async def add_new_address(input_query, full_address, lat, lon):
    async with async_session() as session:
        async with session.begin():
            session.add(
                Address(
                    input_query=input_query,
                    full_address=full_address,
                    latitude=lat,
                    longitude=lon
                )
            )
