import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

log_formatter = '%(asctime)s [%(levelname)s] [%(filename)s] [line:%(lineno)d] %(message)s'
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter(log_formatter))
stream_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)

logger.debug("hello")