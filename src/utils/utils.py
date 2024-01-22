import functools
import time
from typing import Callable, Any


def clean_url(url: str) -> str:
    if not any([url.startswith('http://'), url.startswith('https://')]):
        return 'https://' + url
    else:
        return url


def timed_it(func: Callable) -> Callable:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time()
        if isinstance(result, dict):
            result['script_loading_sec'] = f'{end - start:.4f}'
        return result

    return wrapper
