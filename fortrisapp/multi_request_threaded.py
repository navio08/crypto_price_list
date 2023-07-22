#!/usr/bin/python

import requests
import concurrent.futures
import time


def get_status(url):
    resp = requests.get(url=url)
    return resp.text


urls = ['http://localhost:8081/latest?limit=1', 'http://localhost:8082/ranklatest?limit=2']


tm1 = time.perf_counter()

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(get_status, url=url) for url in urls]
    for future in concurrent.futures.as_completed(futures):
        print(future.result())

tm2 = time.perf_counter()
print(f'Total time elapsed: {tm2-tm1:0.2f} seconds')
