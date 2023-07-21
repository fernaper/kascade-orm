import asyncio

from kascade.base import Kascade


async def main():
    async with Kascade() as db:
        pass


if __name__ == '__main__':
    asyncio.run(main())
