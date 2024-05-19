import logging


def setup_logger(log_file='error.log'):
    """Настройка логгера"""
    # Создание объекта логгера
    slogger = logging.getLogger('error_logger')
    slogger.setLevel(logging.ERROR)  # Установка уровня логгирования на ERROR

    # Создание обработчика для записи логов в файл
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.ERROR)  # Установка уровня логгирования на ERROR

    # Создание форматировщика для логов
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Добавление обработчика к логгеру
    slogger.addHandler(file_handler)

    return slogger


# Инициализация логгера
logger = setup_logger()


# Функция для логирования ошибок
def log_error(error_msg):
    """Логирование ошибки"""
    logger.error(error_msg)


# Функция для логирования ошибок в отдельный файл
def log_tests_error(error_msg):
    """Логирование ошибки в отдельный файл"""
    # Создание объекта логгера для тестовых ошибок
    test_logger = logging.getLogger('tests_error_logger')
    test_logger.setLevel(logging.ERROR)  # Установка уровня логгирования на ERROR

    # Создание обработчика для записи логов в файл error_tests.log
    file_handler = logging.FileHandler('error_tests.log')
    file_handler.setLevel(logging.ERROR)  # Установка уровня логгирования на ERROR

    # Создание форматировщика для логов
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Добавление обработчика к логгеру для тестовых ошибок
    test_logger.addHandler(file_handler)

    # Логирование сообщения об ошибке
    test_logger.error(error_msg)


# Функция для логирования информации в отдельный файл
def log_tests_info(info_msg):
    """Логирование информации в отдельный файл"""
    # Создание объекта логгера для тестовой информации
    test_logger = logging.getLogger('tests_info_logger')
    test_logger.setLevel(logging.INFO)  # Установка уровня логгирования на INFO

    # Создание обработчика для записи логов в файл error_tests.log
    file_handler = logging.FileHandler('error_tests.log')
    file_handler.setLevel(logging.INFO)  # Установка уровня логгирования на INFO

    # Создание форматировщика для логов
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Добавление обработчика к логгеру для тестовой информации
    test_logger.addHandler(file_handler)

    # Логирование информационного сообщения
    test_logger.info(info_msg)
