import logging


def get_failed_url_logger():
  failed_url_logger = logging.getLogger('failed_url_logger')

  failed_url_logger.setLevel(logging.ERROR)

  file_handler = logging.FileHandler("failed_urls.log")
  file_handler.setLevel(logging.ERROR)

  formatter = logging.Formatter(
      '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  file_handler.setFormatter(formatter)

  failed_url_logger.addHandler(file_handler)

  return failed_url_logger
