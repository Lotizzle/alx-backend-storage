#!/usr/bin/env python3
"""
a Python function that changes all topics
of a school document based on the name.
"""


def update_topics(mongo_collection, name, topics):
    """
    Updates the topics of a school document based on the name.

    Args:
        mongo_collection: The collection object.
        name (str): The school name to update.
        topics (list): The list of topics to set for the school.

    Returns:
        None
    """
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
