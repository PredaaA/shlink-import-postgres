import asyncio
import uvloop
import logging
import os

uvloop.install()

import asyncmy
import asyncpg

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

log = logging.getLogger(__name__)


async def get_short_urls(conn: asyncmy.Connection) -> list[dict]:
    async with conn.cursor() as cursor:
        await cursor.execute(
            """
            SELECT author_api_key_id, original_url, short_code, date_created
            FROM short_urls
            """
        )
        return await cursor.fetchall()


async def insert_short_urls(conn: asyncpg.Connection, data: list) -> None:
    await conn.executemany(
        """
        INSERT INTO short_urls (author_api_key_id, original_url, short_code, date_created, forward_query)
        VALUES ($1, $2, $3, $4, false)
        """,
        data,
    )


async def main():
    log.info("Starting...")

    mariadb: asyncmy.Connection = await asyncmy.connect(
        host=os.getenv("MARIADB_HOST"),
        user=os.getenv("MARIADB_USER"),
        password=os.getenv("MARIADB_PASSWORD"),
        db=os.getenv("MARIADB_DB"),
    )
    postgres = await asyncpg.connect(
        host=os.getenv("POSTGRES_HOST"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        database=os.getenv("POSTGRES_DB"),
    )

    short_urls = await get_short_urls(mariadb)
    log.info(f"Got {len(short_urls)} short urls")

    await insert_short_urls(postgres, short_urls)
    log.info("Inserted short urls")

    await postgres.close()


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    loop.run_until_complete(main())
except KeyboardInterrupt:
    log.info("Stopping...")

loop.close()
