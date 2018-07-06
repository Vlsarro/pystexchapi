import time
import random


__all__ = ('make_nonce',)


def make_nonce(makeweight=1000000) -> int:
    if not isinstance(makeweight, int) or makeweight < 0:
        raise ValueError(makeweight)
    return int(time.time()) * makeweight + random.randint(0, makeweight)
