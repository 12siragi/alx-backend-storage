#!/usr/bin/env python3
"""
A module to retrieve web pages and cache the results in Redis.
"""

import requests
import redis
import time

# Initialize the Redis client
cache = redis.Redis()

def cache_page(url: str):
    """
    Decorator to cache the page content and access count in Redis.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Cache key for the URL
            cache_key = f"count:{url}"
            cached_content = cache.get(url)

            # If the page is cached, increment the access count and return cached content
            if cached_content:
                cache.incr(cache_key)
                return cached_content.decode('utf-8')

            # Call the actual function if not cached
            page_content = func(*args, **kwargs)
            # Cache the content with a 10-second expiration
            cache.setex(url, 10, page_content)

            # Increment the access count
            cache.incr(cache_key)

            return page_content
        return wrapper
    return decorator

@cache_page(url='http://slowwly.robertomurray.co.uk')
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a given URL.
    
    Parameters:
    - url (str): The URL to fetch.

    Returns:
    - str: The HTML content of the page.
    """
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    # Testing the function
    print("Fetching page content...")
    content = get_page('http://slowwly.robertomurray.co.uk/delay/5/url/http://google.com')
    print(content[:100])  # Print the first 100 characters of the content

    # Wait and check the cache expiration
    time.sleep(11)
    print("Fetching page content after cache expiration...")
    content_after_expiration = get_page('http://slowwly.robertomurray.co.uk/delay/5/url/http://google.com')
    print(content_after_expiration[:100])  # Print the first 100 characters again
