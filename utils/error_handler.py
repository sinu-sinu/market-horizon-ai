from tenacity import retry, stop_after_attempt, wait_exponential
import logging

logger = logging.getLogger(__name__)


def retry_on_failure(func):
    """
    Decorator for agent retry logic with exponential backoff
    
    Retries up to 3 times with exponential backoff:
    - 1st retry: 2 seconds
    - 2nd retry: 4 seconds  
    - 3rd retry: 8 seconds (max 10 seconds)
    """
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.warning(f"Retrying {func.__name__} after error: {e}")
            raise
    return wrapper