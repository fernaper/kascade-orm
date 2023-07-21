import asyncio

from kascade.base import Kascade
from kascade.table import Table

class Users(Table):
    pass

async def main():
    async with Kascade() as db:
        print(Users().table_name)


if __name__ == '__main__':
    asyncio.run(main())
