from django.core.cache import cache
from django.conf import settings

CACHE_TTL = getattr(settings, 'CACHE_TTL', 60*5)

def get_or_set_cache(key, func, timeout=CACHE_TTL):
    """
    Try to get data from cache; if not present, call func() and cache it.
    """
    data = cache.get(key)
    if data is None:
        data = func()
        cache.set(key, data, timeout)
    return data