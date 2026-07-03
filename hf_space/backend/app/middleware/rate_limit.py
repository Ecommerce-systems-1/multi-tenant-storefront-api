import time
from dataclasses import dataclass, field

@dataclass
class Bucket:
    window_start: float = field(default_factory=time.time)
    count: int = 0

class RateLimiter:
    def __init__(self, limit: int = 60, window_seconds: float = 60.0):
        self.limit = limit
        self.window = window_seconds
        self._buckets: dict[str, Bucket] = {}

    def check(self, tenant_id: str) -> bool:
        now = time.time()
        bucket = self._buckets.get(tenant_id)
        if bucket is None or (now - bucket.window_start) >= self.window:
            self._buckets[tenant_id] = Bucket(window_start=now, count=1)
            return True
        if bucket.count >= self.limit:
            return False
        bucket.count += 1
        return True