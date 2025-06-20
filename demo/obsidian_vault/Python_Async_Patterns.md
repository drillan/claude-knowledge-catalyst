---
title: Python Async Programming Patterns
tags: [python, async, backend, programming, patterns]
created: 2024-01-25
author: Backend Team
projects: [api-development]
---

# Python Async Programming Patterns

## Basic Async/Await

```python
import asyncio
import aiohttp

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def main():
    data = await fetch_data('https://api.example.com/data')
    print(data)

asyncio.run(main())
```

## Concurrent Processing

```python
async def process_urls(urls):
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

# Process multiple URLs concurrently
urls = ['https://api1.com', 'https://api2.com', 'https://api3.com']
results = await process_urls(urls)
```

## Error Handling

```python
async def safe_fetch(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {'error': f'HTTP {response.status}'}
    except asyncio.TimeoutError:
        return {'error': 'Request timeout'}
    except Exception as e:
        return {'error': str(e)}
```
