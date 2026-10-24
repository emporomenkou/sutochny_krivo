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
    @wraps(func)  # Чисто и элегантно возвращает имя функции без ручных костылей
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            # Выполняем функцию и сохраняем то, что она возвращает
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # Записываем в parser.log: Функция - Время - Результат
            logging.info(f"{func.__name__} - {execution_time:.2f} сек. - Результат: {result}")
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            # Если функция упала, вместо результата запишется текст ошибки
            error_msg = f"ОШИБКА: {type(e).__name__} ({str(e)})"
            logging.info(f"{func.__name__} - {execution_time:.2f} сек. - {error_msg}")
            raise e
            
    return wrapper