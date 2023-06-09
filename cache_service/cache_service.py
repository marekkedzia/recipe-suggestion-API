from typing import Callable, Dict, List, TypeVar
from datetime import timedelta, datetime

DAY = timedelta(days=1)
T = TypeVar('T')


class CacheService:
    def __init__(self):
        self.cache: Dict[str, Cache] = {}

    async def get(self, cache_key: str, provider: Callable[[], List[T]], ttl_ms: timedelta = DAY) -> \
            List[T]:
        if cache_key in self.cache and self.cache[cache_key].ttl >= datetime.now():
            return self.cache[cache_key].data

        data = provider()
        self.cache[cache_key] = Cache(ttl=datetime.now() + ttl_ms, data=data)
        return data


class Cache:
    def __init__(self, ttl: datetime, data: List[T]):
        self.ttl = ttl
        self.data = data
