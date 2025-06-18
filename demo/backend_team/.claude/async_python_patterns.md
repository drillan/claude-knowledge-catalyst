---
title: "Async Python Patterns"
project: "Backend-Team"
tags: ["code", "python", "async", "performance"]
category: "code"
status: "production"
author: "Backend Architecture Team"
purpose: "Best practices for async Python development in high-performance applications"
model: "claude-sonnet"
success_rate: 95
---

# Async Python Patterns

## Database Operations
```python
import asyncio
import aiopg

async def fetch_user_data(user_ids):
    """Fetch multiple users concurrently."""
    async with aiopg.create_pool(DATABASE_URL) as pool:
        tasks = [
            fetch_single_user(pool, user_id) 
            for user_id in user_ids
        ]
        return await asyncio.gather(*tasks)

async def fetch_single_user(pool, user_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            return await cur.fetchone()
```

## Error Handling
```python
async def robust_api_call(session, url, retries=3):
    """API call with exponential backoff."""
    for attempt in range(retries):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
        except asyncio.TimeoutError:
            if attempt == retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)
```
