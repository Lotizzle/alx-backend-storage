#!/usr/bin/env python3
"""
This module contains the Cache class and the store method
for creating a redis instance.
"""

import redis
import uuid
from functools import wraps
from typing import Union, Callable


def count_calls(method: callable) -> callable:
    """
    This method counts the number of times a method was called
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        This method returns the original value of the method
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs
    and outputs for a particular function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to store input and output history
        """
        method_name = method.__qualname__

        input_args = str(args)
        self._redis.rpush(f"{method_name}:inputs", input_args)
        output = method(self, *args, **kwargs)
        self._redis.rpush(f"{method_name}:outputs", output)
        return output

    return wrapper


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

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        The store method return the value of a random key

        Parameter: data
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Callable = None) -> Union[str, bytes, int, float, None]:
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

    def replay(method: Callable) -> None:
    """
    Display the history of calls of a particular function
    """
    method_name = method.__qualname__
    inputs = cache._redis.lrange(f"{method_name}:inputs", 0, -1)
    outputs = cache._redis.lrange(f"{method_name}:outputs", 0, -1)

    print(f"{method_name} was called {len(inputs)} times:")
    for input_args, output in zip(inputs, outputs):
        print(f"{method_name}(*{input_args.decode('utf-8')}) -> {output.decode('utf-8')}")
