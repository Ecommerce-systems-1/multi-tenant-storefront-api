from app.middleware.rate_limit import RateLimiter
import time

def test_allows_requests_within_limit():
    rl = RateLimiter(limit=5, window_seconds=60)
    for _ in range(5):
        assert rl.check("tenant1") is True

def test_rejects_over_limit():
    rl = RateLimiter(limit=5, window_seconds=60)
    for _ in range(5):
        rl.check("tenant1")
    assert rl.check("tenant1") is False

def test_tenants_have_independent_buckets():
    rl = RateLimiter(limit=2, window_seconds=60)
    rl.check("t1"); rl.check("t1")
    assert rl.check("t1") is False
    assert rl.check("t2") is True  # t2 unaffected

def test_window_resets_after_expiry():
    rl = RateLimiter(limit=2, window_seconds=0.1)
    rl.check("t1"); rl.check("t1")
    time.sleep(0.15)
    assert rl.check("t1") is True  # window expired