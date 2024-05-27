#!/usr/bin/env python3
"""
This web module contains a get_page function which
uses the requests module to obtain the HTML content of a
particular URL and returns it
"""

import redis
import requests
from functools import wraps
from typing import Callable

# Initialize Redis client
redis_client = redis.Redis()

def cache_page(expiration: int = 10) -> Callable:
    """
    Decorator to cache the result of get_page function.
    """
    def decorator(func: Callable) -> Callable:
        """
        Decorator for cache_page
        """
        @wraps(func)
        def wrapper(url: str) -> str:
            """
            Wrapper to conserve the original
            function’s name, docstring, etc.
            """
            cache_key = f"cache:{url}"
            count_key = f"count:{url}"

            # Increment the count for this URL
            redis_client.incr(count_key)

            # Check if the result is already cached
            cached_result = redis_client.get(cache_key)
            if cached_result:
                return cached_result.decode('utf-8')

            # Fetch the page content
            result = func(url)

            # Cache the result with an expiration time
            redis_client.setex(cache_key, expiration, result)

            return result
        return wrapper
    return decorator

@cache_page(expiration=10)
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a URL and cache the result.
    """
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"
    print(get_page(url))
    print(get_page(url))
    print(f"Access count: {redis_client.get(f'count:{url}').decode('utf-8')}")

