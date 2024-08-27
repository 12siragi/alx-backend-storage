#!/usr/bin/env python3
"""
This module contains a Python script that provides some stats about Nginx logs
stored in MongoDB.
Database: logs
Collection: nginx
Display:
    - First line: x logs where x is the number of documents in this collection
    - Second line: Methods:
        5 lines with the number of documents with the method = ["GET", "POST", "PUT",
        "PATCH", "DELETE"] in this order (see example below - warning: it’s a
        tabulation before each line)
    - One line with the number of documents with:
        method=GET
        path=/status
"""

from pymongo import MongoClient

def log_stats(mongo_collection):
    """
    This function provides some stats about Nginx logs stored in MongoDB.
    """
    # Count total number of logs
    total_logs = mongo_collection.count_documents({})
    print("{} logs".format(total_logs))

    # Count number of documents for each method
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        documents = mongo_collection.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, documents))
    
    # Count number of documents where method=GET and path=/status
    status = mongo_collection.count_documents({"method": "GET", "path": "/status"})
    print("{} status check".format(status))

if __name__ == "__main__":
    with MongoClient() as client:
        db = client.logs
        collection = db.nginx
        log_stats(collection)
