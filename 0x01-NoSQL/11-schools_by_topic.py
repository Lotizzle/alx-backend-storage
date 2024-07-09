#!/usr/bin/env python3
"""
Module contains a Python function that returns
the list of school having a specific topic.
"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of schools having a specific topic.

    Args:
        mongo_collection: The collection object.
        topic (str): The topic to search for.

    Returns:
        list: A list of school documents that have the specific topic.
    """
    return list(mongo_collection.find({"topics": topic}))
