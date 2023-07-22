import asyncio

from kascade import Kascade
from kascade.table import Table

class Users(Table):
    name: str
    email: str

async def main():
    async with Kascade() as db:
        print(Users.get_table_name())


if __name__ == '__main__':
    asyncio.run(main())
