#!/usr/bin/env python3
"""
Module contains a Python function that
returns all students sorted by average score.
"""


def top_students(mongo_collection):
    """
    Returns all students sorted by average score.
    mongo_collection will be the pymongo collection object
    Each student document will have an added 'averageScore' field
    """
    students = mongo_collection.aggregate([
        {
            "$project": {
                "name": 1,
                "topics": 1,
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort": {"averageScore": -1}
        }
    ])
    return list(students)
