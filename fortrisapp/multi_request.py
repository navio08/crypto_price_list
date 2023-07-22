#!/usr/bin/python

import httpx
import asyncio
import time


async def get_async(url, limit: int = 1):
    async with httpx.AsyncClient() as client:
        return await client.get(url, params={"limit": limit})

urls = ['http://localhost:8081/latest?limit=1', 'http://localhost:8082/ranklatest?limit=2']


async def launch():
    resps = await asyncio.gather(*map(get_async, urls))
    data = [resp.text for resp in resps]

    for status_code in data:
        print(status_code)

tm1 = time.perf_counter()

asyncio.run(launch())

tm2 = time.perf_counter()
print(f'Total time elapsed: {tm2-tm1:0.2f} seconds')
