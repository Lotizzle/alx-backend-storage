#!/usr/bin/env python3
"""
This module contains a Python function
that lists all documents in a collection.
"""


def list_all(mongo_collection):
    """
    Lists all documents in a MongoDB collection.

    Args:
        mongo_collection: The collection object.

    Returns:
        list: A list of all documents in the collection,
        or an empty list if none are found.
    """
    return list(mongo_collection.find())
