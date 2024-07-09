#!/usr/bin/env python3
"""
a Python function that inserts a new document
in a collection based on kwargs.
"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document into a MongoDB collection.

    Args:
        mongo_collection: The collection object.
        **kwargs: represents the new document's fields.

    Returns:
        ObjectId: The _id of the newly inserted document.
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
