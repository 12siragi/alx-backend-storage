#!/usr/bin/env python3
"""
A function that inserts a new document in a collection
based on kwargs
"""


def insert_school(mongo_collection, **kwargs):
    """
    this function adds a new document to an existing collection
    And returns the new id
    """
    new_doc = mongo_collection.insert_one(kwargs)
    return new_doc.inserted_id
