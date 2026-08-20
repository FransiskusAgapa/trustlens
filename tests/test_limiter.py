from app.rate_limiter import TokenBucket
from unittest.mock import MagicMock

def make_request(forwarded_ip=None, direct_ip="127.0.0.1"):
    mock_request = MagicMock()
    mock_request.headers.get.return_value = forwarded_ip
    mock_request.client.host = direct_ip
    return mock_request

def test_allows_request_when_tokens_available():
    limiter = TokenBucket(capacity=5, refill_rate=1)
    request = make_request()
    assert limiter.is_allowed(request) is True

def test_blocks_request_when_bucket_empty():
    limiter = TokenBucket(capacity=3, refill_rate=1)
    request = make_request()
    limiter.is_allowed(request)
    limiter.is_allowed(request)
    limiter.is_allowed(request)
    assert limiter.is_allowed(request) is False

def test_reads_forwarded_ip_header():
    limiter = TokenBucket(capacity=5, refill_rate=1)
    request = make_request(forwarded_ip="192.168.1.1, 10.0.0.1")
    assert limiter.is_allowed(request) is True
    assert "192.168.1.1" in limiter.clients

def test_different_ips_have_separate_buckets():
    limiter = TokenBucket(capacity=1, refill_rate=1)
    request_a = make_request(direct_ip="1.1.1.1")
    request_b = make_request(direct_ip="2.2.2.2")
    assert limiter.is_allowed(request_a) is True
    assert limiter.is_allowed(request_b) is True