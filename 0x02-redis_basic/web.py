#!/usr/bin/env python3
import redis
import requests
from functools import wraps
from time import time

# Connect to Redis
cache = redis.Redis()

def cache_page(expiration_time: int):
    """Decorator to cache the output of the get_page function."""
    def decorator(func):
        @wraps(func)
        def wrapper(url: str):
            # Check if the URL is cached
            cached_data = cache.get(url)
            if cached_data:
                # If cached, return the cached data
                return cached_data.decode('utf-8')

            # If not cached, call the original function to fetch the page
            html_content = func(url)
            
            # Cache the result with an expiration time
            cache.set(url, html_content, ex=expiration_time)

            # Increment the access count
            count_key = f"count:{url}"
            cache.incr(count_key)

            return html_content
        return wrapper
    return decorator

@cache_page(expiration_time=10)  # Cache the page for 10 seconds
def get_page(url: str) -> str:
    """Fetch the HTML content of a URL.
    
    Args:
        url (str): The URL to fetch.
        
    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text

# Example usage (this can be removed or commented out)
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/3000/url/http://www.google.com"
    print(get_page(url))
