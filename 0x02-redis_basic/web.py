#!/usr/bin/env python3
"""
Script to cache web pages and log access stats.
"""

import redis
import requests
from typing import Callable

# Initialize Redis client
cache = redis.Redis()


def get_page(url: str) -> str:
    """
    Retrieves a URL and caches it in Redis with a 10-second expiration.
    Increments access count for each call.

    Parameters:
    - url (str): The URL to retrieve and cache.

    Returns:
    - str: The content of the URL.
    """
    cached_page = cache.get(url)
    if cached_page:
        cache.incr("page_access_count")
        return cached_page.decode('utf-8')

    response = requests.get(url)
    page_content = response.text

    # Cache the content with a 10-second expiration
    cache.setex(url, 10, page_content)

    # Increment the page access count
    cache.incr("page_access_count")

    return page_content


def log_stats():
    """Logs stats from the nginx logs collection in MongoDB."""
    try:
        from pymongo import MongoClient
    except ModuleNotFoundError:
        print("Error: pymongo module not found.")
        return

    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    total = logs_collection.count_documents({})
    get = logs_collection.count_documents({"method": "GET"})
    post = logs_collection.count_documents({"method": "POST"})
    put = logs_collection.count_documents({"method": "PUT"})
    patch = logs_collection.count_documents({"method": "PATCH"})
    delete = logs_collection.count_documents({"method": "DELETE"})
    path = logs_collection.count_documents({"method": "GET", "path": "/status"})

    print(f"{total} logs")
    print("Methods:")
    print(f"\tmethod GET: {get}")
    print(f"\tmethod POST: {post}")
    print(f"\tmethod PUT: {put}")
    print(f"\tmethod PATCH: {patch}")
    print(f"\tmethod DELETE: {delete}")
    print(f"{path} status check")
    print("IPs:")

    # Aggregate top IPs
    sorted_ips = logs_collection.aggregate(
        [{"$group": {"_id": "$ip", "count": {"$sum": 1}}},
         {"$sort": {"count": -1}}])
    for i, ip in enumerate(sorted_ips):
        if i == 10:
            break
        print(f"\t{ip.get('_id')}: {ip.get('count')}")


if __name__ == "__main__":
    # Test caching functionality
    url = "http://google.com"

    # Fetch and cache page
    print("Fetching page content...")
    page_content = get_page(url)
    print("Page content cached:", bool(cache.get(url)))

    # Wait 10 seconds to test expiration
    from time import sleep
    print("Waiting 10 seconds for cache to expire...")
    sleep(10)
    print("Page content after expiration:", cache.get(url))

    # Log stats from MongoDB
    print("\nLog statistics:")
    log_stats()
