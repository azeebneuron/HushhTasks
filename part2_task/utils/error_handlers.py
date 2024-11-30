# utils/error_handlers.py
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)
import logging
from typing import Type, Callable
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProcessingError(Exception):
    """Base class for processing errors"""
    pass

class APIError(ProcessingError):
    """Raised when API calls fail"""
    pass

class ModelError(ProcessingError):
    """Raised when model processing fails"""
    pass

class ValidationError(ProcessingError):
    """Raised when response validation fails"""
    pass

def create_retry_decorator(
    max_attempts: int = 3,
    min_wait: int = 4,
    max_wait: int = 10,
    exception_types: tuple = (APIError, ModelError)
) -> Callable:
    """
    Create a retry decorator with specified parameters
    
    Args:
        max_attempts (int): Maximum number of retry attempts
        min_wait (int): Minimum wait time between retries
        max_wait (int): Maximum wait time between retries
        exception_types (tuple): Types of exceptions to retry on
        
    Returns:
        Callable: Retry decorator
    """
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=min_wait, max=max_wait),
        retry=retry_if_exception_type(exception_types),
        before_sleep=before_sleep_log(logger, logging.INFO)
    )

# Default retry decorator for API calls
api_retry = create_retry_decorator()

def handle_json_parsing(response_text: str) -> dict:
    """
    Safely parse JSON from response text
    
    Args:
        response_text (str): Text to parse
        
    Returns:
        dict: Parsed JSON object
        
    Raises:
        ValidationError: If JSON parsing fails
    """
    try:
        # Try direct JSON parsing
        return json.loads(response_text)
    except json.JSONDecodeError:
        # Try to extract JSON object from text
        try:
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx == -1 or end_idx == 0:
                raise ValidationError("No JSON object found in response")
            return json.loads(response_text[start_idx:end_idx])
        except (json.JSONDecodeError, ValueError) as e:
            raise ValidationError(f"Failed to parse JSON: {str(e)}")

def log_error(error: Exception, context: str = ""):
    """
    Log error with context
    
    Args:
        error (Exception): Error to log
        context (str): Additional context
    """
    logger.error(f"Error in {context}: {str(error)}", exc_info=True)