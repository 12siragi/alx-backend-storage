#!/usr/bin/env python3
"""
This module contains a Python script that provides some stats about Nginx logs
stored in MongoDB.
"""

from pymongo import MongoClient


def log_stats(mongo_collection):
    """
    Provides some stats about Nginx logs stored in MongoDB.
    """
    total_logs = mongo_collection.count_documents({})
    print(f"{total_logs} logs")
    
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        documents = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {documents}")
    
    status = mongo_collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status} status check")


if __name__ == "__main__":
    with MongoClient() as client:
        db = client.logs
        collection = db.nginx
        log_stats(collection)
