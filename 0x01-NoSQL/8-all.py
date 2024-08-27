#!/usr/bin/env python3
"""A function that lists all documents in a collection"""


def list_all(mongo_collection):
    """This method lists all documents in a collection"""
    return mongo_collection.find()
