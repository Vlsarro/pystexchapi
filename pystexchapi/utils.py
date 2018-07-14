import time
import random


__all__ = ('make_nonce', 'set_not_none_dict_kwargs')


def make_nonce(makeweight: int=1000000) -> int:
    if not isinstance(makeweight, int) or makeweight < 0:
        raise ValueError(makeweight)
    return int(time.time()) * makeweight + random.randint(0, makeweight)


def set_not_none_dict_kwargs(dictionary: dict, **kwargs):
    if dictionary and isinstance(dictionary, dict):
        for k, v in kwargs.items():
            if v is not None:
                dictionary[k] = v
