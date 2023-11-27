import time
from typing import Any, Callable


def calculate_time(func: Callable[..., Any]) -> Any:
    def wrapper(*args: Any, **kwargs: Any):
        t0 = time.time()
        result = func(*args, **kwargs)
        print(f'[{func}]: {time.time() - t0}s')
        return result
    return wrapper