import time
import logging
from django.utils.deprecation import MiddlewareMixin
from ..metrics import blocked_requests_total, response_time_histogram

logger = logging.getLogger(__name__)

class MetricsMiddleware(MiddlewareMixin):
    TRACKED_ENDPOINTS = [
        '/usuario/api/login/',
        '/usuario/api/register/',
        '/emociones/user/emotions/create/'
    ]

    def process_request(self, request):
        logger.debug(f"Processing request to: {request.path}")
        
        # check if this is a tracked endpoint
        for endpoint in self.TRACKED_ENDPOINTS:
            if request.path == endpoint:
                logger.debug(f"Matched tracked endpoint: {endpoint}")
                # record the start time
                request.start_time = time.time()
                break
        return None

    def process_response(self, request, response):
        # get information about the request
        endpoint = request.path  # which url was accessed
        method = request.method  # what type of request (get, post, etc.)
        status = str(response.status_code)  # the response status (200, 401, 403, etc.)

        logger.debug(f"Processing response for: {endpoint}")
        
        # check if this is a tracked endpoint
        for tracked in self.TRACKED_ENDPOINTS:
            if endpoint == tracked:
                logger.debug(f"Matched tracked endpoint for metrics: {tracked}")
                
                # calculate and record the response time
                if hasattr(request, 'start_time'):
                    # calculate how long the request took
                    response_time = time.time() - request.start_time
                    logger.debug(f"Recording response time: {response_time} seconds for {endpoint}")
                    try:
                        # record the response time
                        response_time_histogram.labels(
                            endpoint=endpoint,
                            method=method,
                            status=status
                        ).observe(response_time)
                        logger.debug("Successfully recorded response time metric")
                    except Exception as e:
                        logger.error(f"Error recording response time metric: {str(e)}")

                # check if this was a blocked request (401 unauthorized or 403 forbidden)
                if response.status_code in [401, 403]:
                    reason = 'unauthorized' if response.status_code == 401 else 'forbidden'
                    logger.debug(f"Recording blocked request for {endpoint} with reason: {reason}")
                    try:
                        # increment counter for blocked requests
                        blocked_requests_total.labels(
                            reason=reason,
                            endpoint=endpoint,
                            method=method
                        ).inc()
                        logger.debug("Successfully recorded blocked request metric")
                    except Exception as e:
                        logger.error(f"Error recording blocked request metric: {str(e)}")
                break

        return response 