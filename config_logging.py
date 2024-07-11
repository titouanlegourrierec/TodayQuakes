import time
import logging
from functools import wraps

def configure_logging():
    logging.basicConfig(filename='log/log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='a')
    logging.getLogger('matplotlib').setLevel(logging.ERROR)
    return logging

def log_execution_time(message=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            if message:
                logging.info(f"{message} ({func.__name__} executed in {execution_time:.2f} seconds)")
            else:
                logging.info(f"{func.__name__} executed in {execution_time:.2f} seconds")
            return result
        return wrapper
    return decorator