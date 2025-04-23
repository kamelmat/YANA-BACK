from prometheus_client import Counter, Histogram, REGISTRY
from prometheus_client.core import CollectorRegistry
import logging

logger = logging.getLogger(__name__)

registry = CollectorRegistry()

try:
    # define a counter for tracking blocked requests
    # this will count how many times requests are blocked (401 unauthorized or 403 forbidden)
    # it includes labels for:
    # - reason: why the request was blocked
    # - endpoint: which url was blocked
    # - method: what type of request (get, post, etc.)
    blocked_requests_total = Counter(
        'blocked_requests_total',  # name of the metric
        'total number of blocked requests',  # description
        ['reason', 'endpoint', 'method'],  # labels to track
        namespace='yana',  # prefix for metrics
        registry=registry  # where to store this metric
    )
    logger.debug("Successfully initialized blocked_requests_total metric")

    # define a histogram for tracking response times
    # this measures how long each request takes to process
    # the buckets define time ranges for grouping response times:
    # 1.0s, 2.0s, 5.0s, 10.0s, and anything above
    response_time_histogram = Histogram(
        'response_time_seconds',
        'response time in seconds',
        ['endpoint', 'method', 'status'],
        namespace='yana', 
        buckets=(1.0, 2.0, 5.0, 10.0, float('inf')),  # time ranges
        registry=registry  # where to store this metric
    )
    logger.debug("Successfully initialized response_time_histogram metric")
except Exception as e:
    logger.error(f"Error initializing metrics: {str(e)}")
    raise 