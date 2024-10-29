#!/usr/bin/env python3
"""
This module provides stats about Nginx logs stored in MongoDB.
"""

from pymongo import MongoClient

def log_stats(mongo_collection):
    """
    Provides stats about Nginx logs stored in MongoDB
    """
    total_logs = mongo_collection.count_documents({})
    print(f"{total_logs} logs")
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")
    status_check = mongo_collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check} status check")

if __name__ == "__main__":
    client = MongoClient()
    db = client.logs
    collection = db.nginx
    log_stats(collection)

