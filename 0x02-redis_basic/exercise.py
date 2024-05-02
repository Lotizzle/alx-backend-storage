#!/usr/bin/env python3
"""
This module contains the Cache class and the store method
for creating a redis instance.
"""

import redis
import uuid
from typing import Union


class Cache:
    """
    This class creates a redis instance.
    """

    def __init__(self):
        """
        Initialization method
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        The store method return the value of a random keyy
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
