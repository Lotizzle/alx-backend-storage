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
        The store method return the value of a random key

        Parameter: data
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        """
        This method takes a key string argument and
        an optional Callable argument named fn

        Parameter: key, fn
        """
        if fn is None:
            return self._redis.get(key)
        else:
            data = self._redis.get(key)
            if data is None:
                return None
            else:
                return fn(data)

    def get_str(self, key: str) -> Union[str, None]:
        """
        This method automatically parametrizes Cache.get to
        return a string object

        Parameter: key
        """
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Union[int, None]:
        """
        This method automatically parametrizes Cache.get
        to return an int object
        """
        return self.get(key, fn=lambda d: int(d))
