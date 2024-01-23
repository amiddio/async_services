import time
from typing import Callable, Any
from urllib.parse import urlparse


def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def timed_it(func: Callable) -> Callable:
    async def wrapper(*args, **kwargs) -> Any:
        start = time.time()
        result = await func(*args, **kwargs)
        if isinstance(result, dict):
            result['script_loading_sec'] = f'{time.time() - start:.4f}'
        return result

    return wrapper
