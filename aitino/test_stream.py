import aiohttp
import asyncio
import json
import sys


async def call_maeve(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            while True:
                line = await response.content.readline()
                await asyncio.sleep(0.1)
                if not line:
                    break
                yield line.decode("utf-8")


async def main():
    if len(sys.argv) != 2:
        print("Usage: python test.py <url>")
        return

    url = sys.argv[1]

    i = 0
    async for event in call_maeve(url):
        i += 1
        print(json.dumps(json.loads(event.strip()), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
