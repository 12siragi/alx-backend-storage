#!/usr/bin/env python3
"""
Module web.py
Provides a function to fetch and cache the HTML content of a URL.
Includes a decorator to track URL accesses and cache the content with an expiration time.
"""

import redis
import requests
from typing import Callable
from functools import wraps

# Initialize Redis client
redis_client = redis.Redis()

def cache_page(expiration: int = 10) -> Callable:
    """
    Decorator to cache the page content and count URL accesses.

    Args:
        expiration (int): Time in seconds for the cache to expire.

    Returns:
        Callable: Wrapped function with caching and access counting.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            """
            Wrapper function to cache content and count access.

            Args:
                url (str): The URL to fetch and cache.

            Returns:
                str: The HTML content of the URL.
            """
            # Track the number of times the URL is accessed
            cache_count_key = f"count:{url}"
            redis_client.incr(cache_count_key)

            # Check if the result is already cached
            cache_content_key = f"cached:{url}"
            cached_content = redis_client.get(cache_content_key)
            if cached_content:
                return cached_content.decode('utf-8')

            # Fetch the page content
            content = func(url)

            # Cache the content with an expiration time
            redis_client.setex(cache_content_key, expiration, content)
            return content

        return wrapper

    return decorator

@cache_page(expiration=10)
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a given URL and cache it.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    # Example usage
    url = "http://slowwly.robertomurray.co.uk"
    print(get_page(url))
    print(f"Access count: {redis_client.get(f'count:{url}').decode('utf-8')}")
