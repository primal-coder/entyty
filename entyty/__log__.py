import logging
from functools import wraps

logging.addLevelName(37, "ENTITY")
logger = logging.getLogger("ENTITY")
file_handler = logging.FileHandler('entity.log')
file_handler.setLevel(37)
formatter = logging.Formatter('%(asctime)s - %(message)s', 'w')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(37)

def log(message):
    logger.log(37, message)

def log_method(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        log(f'Calling {func.__name__}(args={args}, kwargs={kwargs})')
        return func(*args, **kwargs)
    return wrapper
