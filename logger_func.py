import time
import logging
from functools import wraps

LOG_FILE = "parser.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8")
    ]
)

def logger(func):
    @wraps(func)  # Чисто возвращает имя функции
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            logging.info(f"{func.__name__} - {execution_time:.2f} сек. - Результат: {result}")
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"ОШИБКА: {type(e).__name__} ({str(e)})"
            logging.info(f"{func.__name__} - {execution_time:.2f} сек. - {error_msg}")
            raise e
            
    return wrapper

def clean_logs():
    with open('parser.log', 'w', encoding='utf-8') as f:
        f.truncate(0)