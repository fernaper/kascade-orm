import asyncio

from base import Kascade


async def main():
    async with Kascade() as db:
        print('main')


if __name__ == '__main__':
    asyncio.run(main())
